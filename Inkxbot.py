from discord.ext import commands
import discord
import datetime
import re
import json, asyncio
import copy
import logging
import traceback
import sys
from collections import Counter


description = '''
    My command list is right here, each is used with 2 commas
    '''


# this specifies what extensions to load when the bot starts up
startup_extensions = ["Inkxbotcogs.SplatoonCog",
                      "Inkxbotcogs.JustdanceCog",
                      "Inkxbotcogs.HearthstoneCog",
                      "Inkxbotcogs.DestinyCog",
                      "Inkxbotcogs.admin",
                      "Inkxbotcogs.modcog",
                      "Inkxbotcogs.MiscCog"
                      ]



help_attrs = dict(hidden=True)
prefix = [',,', '-']
bot = commands.Bot(command_prefix=',,', description=description, pm_help=True, help_attrs=help_attrs)


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
    print('--------------------------------')
    await bot.change_presence(game=discord.Game(name='https://inkxbot.wordpress.com/'))
    #await bot.send_message(discord.Object(id='248106639410855936'), "@here, A new WordPress post about my development has been made, check it out at <https://inkxbot.wordpress.com/>")
    #await bot.send_message(discord.Object(id='227514633735372801'), "A new WordPress post about my development has been made, check it out at <https://inkxbot.wordpress.com/>")
    #await bot.send_message(discord.Object(id='258350226279104512'), "A new WordPress post about my development has been made, check it out at <https://inkxbot.wordpress.com/>")


@bot.event
async def on_member_ban(member):
    for channel in member.server.channels:
        if channel.name == "ban-logs":
            await bot.send_message(channel, content="**BAN** \n**User**: {0}".format(member))
            break
@bot.event
async def on_message(message):
    #~ lm = load_messages()
    #~ server = message.server
    #~ svr = lm[server.id]
    #~ author = message.author.mention
    #~ shill = lm[server.id]["severShill"]
    #~ forbode = lm[server.id]["forbode"]
    #~ shillmsg = shill.format(author)
    #~ fbmsg = forbode.format(author)
	#~ notdeadem = discord.Embed(title="", color=0xFF8C00))

    if message.content.startswith('+rip Inkxbot'):
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

    elif message.content.startswith('<@245648163837444097>'):
        await bot.send_typing(message.channel)
        await asyncio.sleep(1)
        await bot.send_message(message.channel, "What the hell do you want from me. ~~type ,,inkxbot you nerd~~")

    elif message.content.startswith('(╯°□°）╯︵ ┻━┻'):    
        await bot.send_typing(message.channel)
        await asyncio.sleep(1)
        await bot.send_message(message.channel, "┬─┬﻿ ノ( T_Tノ)")

    elif message.content.startswith('/tableflip'):
        await bot.send_typing(message.channel)
        await asyncio.sleep(1)
        await bot.send_message(message.channel, "┬─┬﻿ ノ( T_Tノ)")
        

    #~ elif invite_syntax.search(message.content):
        #~ if server.id == svr:
            #~ if server.id not in svr: return
            #~ if "forbode" not in svr: return
            #~ await bot.send_message(message.channel, fbmsg)
            #~ await asyncio.sleep(1)
            #~ await bot.send_message(message.channel, shillmsg)

    await bot.process_commands(message)

def load_credentials():
    with open('credentials.json') as f:
        return json.load(f)

if __name__ == '__main__':
    credentials = load_credentials()
    token = credentials['token']    
    bot.client_id = credentials['client_id']
    bot.commands_used = Counter()
#    bot.carbon_key = credentials['carbon_key']
#    bot.bots_key = credentials['bots_key']
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print('Failed to load extension {}\n{}: {}'.format(extension, type(e).__name__, e))

    bot.run(token)
