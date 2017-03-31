from discord.ext import commands
from Inkxbotcogs.utils import checks
import discord
import datetime
import re
import json, asyncio
import aiohttp
import copy
import logging
import traceback
import sys
import subprocess
from collections import Counter


description = 'My command list is right here, each is used with a comma' # or a period' (in the future)


# this specifies what extensions to load when the bot starts up
startup_extensions = ["Inkxbotcogs.SplatoonCog",
                      "Inkxbotcogs.JustdanceCog",
                      "Inkxbotcogs.HearthstoneCog",
                      "Inkxbotcogs.DestinyCog",
                      "Inkxbotcogs.admin",
                      "Inkxbotcogs.modcog",
                      "Inkxbotcogs.MiscCog",
                      "Inkxbotcogs.dbots",
                      "Inkxbotcogs.ScoresForBattles",
                      "Inkxbotcogs.MetaCog",
                      "Inkxbotcogs.ChallongeCog",
                      "Inkxbotcogs.StatsCog"
                      ]


discord_logger = logging.getLogger('discord')
discord_logger.setLevel(logging.CRITICAL)
log = logging.getLogger()
log.setLevel(logging.INFO)
handler = logging.FileHandler(filename='inkxbot.log', encoding='utf-8', mode='w')
log.addHandler(handler)

help_attrs = dict(hidden=True)


# this line below is for future purposes, it's not gonna be used yet
#prefix = [',', '.']u

bot = commands.Bot(command_prefix=',', description=description, pm_help=True, help_attrs=help_attrs)


def load_messages():
    with open('servermessage.json') as m:
        return json.load(m)

@bot.event
async def on_member_join(member):
    server = member.server
    messages = load_messages()
    if server.id not in messages: return
    if "welcome" not in messages[server.id]: return
    srv = messages[server.id]
    wlc = messages[server.id]['welcome'].format(member)
    await bot.send_message(server, wlc)

@bot.event
async def on_ready():
    print('Inkxbot is logged in and online!')
    print("discord.py version is " + discord.__version__)
    print('--------------------------------')
    if not hasattr(bot, 'uptime'):
        bot.uptime = datetime.datetime.utcnow()
    await bot.change_presence(game=discord.Game(name='https://inkxbot.wordpress.com'))

@bot.event
async def on_member_ban(member):
    for channel in member.server.channels:
        if channel.name == "banlogs":
            await bot.send_message(channel, content="**BAN** \n**User**: {0}".format(member))
            break

@bot.event
async def on_message(message):
    # lm = load_messages()
    server = message.server
    # svr = lm[server.id]
    # author = message.author.mention
    # shill = lm[server.id]["severShill"]
    # forbode = lm[server.id]["forbode"]
    # shillmsg = shill.format(author)
    # fbmsg = forbode.format(author)
	# notdeadem = discord.Embed(title="", color=0xFF8C00))


    if message.author.bot:
        return
    elif message.content.startswith('+rip Inkxbot'):
        await asyncio.sleep(8)
        await bot.send_typing(message.channel)
        await asyncio.sleep(2)
        await bot.send_message(message.channel, "That's a lie.")

    elif message.content.startswith('+rip <@245648163837444097>'):
        await asyncio.sleep(8)
        await bot.send_typing(message.channel)
        await asyncio.sleep(2)
        await bot.send_message(message.channel, "That's a lie.")

    elif message.content.startswith('+kill <@245648163837444097>'):
        await asyncio.sleep(8)
        await bot.send_typing(message.channel)
        await asyncio.sleep(1)
        await bot.send_message(message.channel, "Sticks and Stones may break my bolts, but lazer cannons never hurt me.")

    elif message.content.startswith('+kill Inkxbot'):
        await asyncio.sleep(8)
        await bot.send_typing(message.channel)
        await asyncio.sleep(1)
        await bot.send_message(message.channel, "Sticks and Stones may break my bolts, but lazer cannons never hurt me.")

    elif message.content.startswith('(╯°□°）╯︵ ┻━┻'):
        if server.id == "110373943822540800":
            await asyncio.sleep(1)
        else:
            await bot.send_message(message.channel, "┬─┬ ノ( T_Tノ)")

    elif message.content.startswith('/tableflip'):
        if server.id == "110373943822540800": # the mods on Dbots don't want the bot to respond there
            await asyncio.sleep(1)
        else:
            await bot.send_message(message.channel, "┬─┬ ノ( T_Tノ)")


    # elif invite_syntax.search(message.content):
        # if server.id == svr:
            # if server.id not in svr: return
            # if "forbode" not in svr: return
            # await bot.send_message(message.channel, fbmsg)
            # await asyncio.sleep(1)
            # await bot.send_message(message.channel, shillmsg)

    await bot.process_commands(message)


@bot.event
async def on_resumed():
    print('resumed...')

@bot.command(pass_context=True, hidden=True)
@checks.is_owner()
async def do(ctx, times : int, *, command):
    """Repeats a command a specified number of times."""
    msg = copy.copy(ctx.message)
    msg.content = command
    for i in range(times):
        await bot.process_commands(msg)



def load_credentials():
    with open('credentials.json') as f:
        return json.load(f)



if __name__ == '__main__':
    credentials = load_credentials()
    token = credentials['token']
    bot.client_id = credentials['client_id']
    bot.carbon_key = credentials['carbon_key']
    bot.discordlist_token = credentials['discordlist_token']
    bot.dbots_key = credentials['dbots_key']
    bot.commands_used = Counter()
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print('Failed to load extension {}\n{}: {}'.format(extension, type(e).__name__, e))
    bot.run(token)
    handlers = log.handlers[:]
    for hdlr in handlers:
        hdlr.close()
        log.removeHandler(hdlr)
