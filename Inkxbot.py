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


description = '''My command list is right here'''


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
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(game=discord.Game(name='https://inkxbot.wordpress.com/'))
    #await bot.send_message(discord.Object(id='248106639410855936'), "@here, A new WordPress post about my development has been made, check it out at https://inkxbot.wordpress.com/")
    #await bot.send_message(discord.Object(id='227514633735372801'), "A new WordPress post about my development has been made, check it out at https://inkxbot.wordpress.com/")
    #await bot.send_message(discord.Object(id='258350226279104512'), "A new WordPress post about my development has been made, check it out at https://inkxbot.wordpress.com/")


@bot.command()
async def join():
    """I will give you a link so I can be added to a server"""
    await bot.say('You want me to join a server? Ok! Add me to a server by using this link: https://discordapp.com/oauth2/authorize?client_id=245648163837444097&scope=bot&permissions=268437512')

@bot.command()
async def inkxbot():
    """All about me!"""
    await bot.say("Hi! I'm Inkxbot! I was created by InkxtheSquid to be used as a tool for many purposes! type ``,,help`` to see my list of commands! Inkxbot discord server: https://discord.gg/MzCCN5b (Note: all my commands are not implemented yet, so I'm not finished yet)")

@bot.group(pass_context=True)
async def rip(ctx):
    """I will post a rip message"""
    if ctx.invoked_subcommand is None:
        await bot.say('rip indeed man'.format(ctx))

@rip.command(name='Inkxbot', hidden=True)
async def _bot():
    """Is the bot dead?"""
    await bot.say("Dumba$$, I'm not dead.")

@rip.command(name='inkxbot', hidden=True)
async def _bot():
    """Is the bot dead?"""
    await bot.say("Dumba$$, I'm not dead.")

@rip.command(name='<@245648163837444097>', hidden=True)
async def _bot():
    """Is the bot dead?"""
    await bot.say("Dumba$$, I'm not dead.")



#@bot.command()
#async def kill(ctx, args):
#    """Kill someone!"""
#    user = ctx.message.author
#    if args is True:
#        await bot.say('{1} has taught {0.name} a new emotion, ``Rage``, {0.name} wants to stop {1}, {0.name} wants to hurt {1}, {0.name} wants to **kill** {1}... *{0.name} kills {1}*'.format(user, args))
#    elif args == '@everyone':
#        await bot.say("Absolutely not.")
#    elif args == '@here':
#        await bot.say("Absolutely not.")
#    elif args == 'Inkxbot':
#        await bot.say('{0.name) tries to kill @{1}, But suddenly, @{1} grabs {0.name} tightly by the wrist and says,"Just what do you think you are doing?" *@{1} kills his attacker*'.format(user, args))
#    elif args == '<@245648163837444097>':
#        await bot.say('{0.name) tries to kill {1}, But suddenly, {1} grabs {0.name} tightly by the wrist and says,"Just what do you think you are doing?" *{1} kills his attacker*'.format(user, args))

@bot.command(pass_context=True)
async def slap(ctx, args):
    """Slap someone!"""
    user = ctx.message.author.mention
    await bot.say('**SMACK!** *{0} slaps {1}*'.format(user, args)) 

@bot.event
async def on_member_ban(member):
    for channel in member.server.channels:
        if channel.name == "ban-logs":
            await bot.send_message(channel, content="**BAN** \n**User**: {0}".format(member))
            break
    else:
        await bot.send_message(member.server.channels[0], "hey, I noticed that you made a ban, want to keep records of your server's bans? Create a ``ban-logs`` text channel for me to keep track of the server's bans!")

@bot.event
async def on_message(message, ctx):

    invite_syntax = re.compile(r'((http|https):\/\/)?discord.gg\/([a-z0-9])+', re.IGNORECASE)
    lm = load_messages()
    svr = lm[server.id]
    author = ctx.message.author.mention
    shill = svr["severShill"]
    forbode = svr["forbode"]
    shillmsg = shill.format(author)
    fbmsg = forbode.format(author)

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
        

    elif invite_syntax.search(message.content):
        if message.server.id == svr:
            if server.id not in lm: 
                return
            else:
                if "forbode" not in svr:
                    await bot.send_message(message.channel, shillmsg)
                else:
                    await bot.send_message(message.channel, fbmsg)
                    await asyncio.sleep(1)
                    await bot.send_message(message.channel, shillmsg)

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
