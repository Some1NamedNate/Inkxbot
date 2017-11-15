from collections import Counter
import traceback
import datetime
import logging
import asyncio
import copy
import json
import sys
import os

from discord.ext import commands
import discord


description = 'My command list is right here, each is used with a comma' # or a period' (in the future)


# this specifies what extensions to load when the bot starts up
startup_extensions = ["cogs.JustdanceCog",
                      "cogs.SplatoonCog",
                      "cogs.HearthstoneCog",
                      "cogs.DestinyCog",
                      "cogs.admin",
                      "cogs.BackgroundtaskCog",
                      "cogs.modcog",
                      "cogs.MiscCog",
                      "cogs.dbots",
                      "cogs.ScoresForBattles",
                      "cogs.MetaCog",
                      "cogs.ChallongeCog",
                      "cogs.EasterEggs",
                      "cogs.StatsCog"
                      ]


discord_logger = logging.getLogger('discord')
discord_logger.setLevel(logging.CRITICAL)
log = logging.getLogger()
log.setLevel(logging.INFO)
handler = logging.FileHandler(filename='inkxbot.log', encoding='utf-8', mode='w')
log.addHandler(handler)

help_attrs = dict(hidden=True)

botfmt = commands.HelpFormatter(show_check_failure=True)

# this line below is for future purposes, it's not gonna be used yet
#prefix = [',', '.']

bot = commands.Bot(command_prefix=',', description=description, pm_help=True, help_attrs=help_attrs, formatter=botfmt)


def load_messages():
    with open('servermessage.json') as m:
        return json.load(m)

@bot.event
async def on_member_join(member):
    guild = member.guild
    messages = load_messages()
    guildstr = str(guild.id)
    if guildstr not in messages: return
    if 'welcome' not in messages[guildstr]: return
    srv = messages[guildstr]
    chanid = srv['channel']
    channel = bot.get_channel(chanid)
    wlc = messages[guildstr]['welcome'].format(member)
    await channel.send(wlc)

@bot.event
async def on_ready():
    print('Inkxbot is logged in and online!')
    print("discord.py version is " + discord.__version__)
    print('--------------------------------')
    if not hasattr(bot, 'uptime'):
        bot.uptime = datetime.datetime.utcnow()


@bot.event
async def on_member_ban(guild, user):
    for channel in guild.channels:
        if channel.name == "banlogs":
            await channel.send("**BAN** \n**User**: {0}".format(user))
            break
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error):
    channel = ctx.message.channel
    author  = ctx.message.author
    ignored = (commands.CommandNotFound, commands.UserInputError)
    error = getattr(error, 'original', error)
    if isinstance(error, ignored):
        return
    elif isinstance(error, commands.NoPrivateMessage):
        await discord.User.trigger_typing(author)
        await asyncio.sleep(1)
        await author.send("Hey! This command can't be used in DMs.")
    elif isinstance(error, commands.DisabledCommand):
        channel = ctx.message.channel
        await channel.trigger_typing()
        await asyncio.sleep(1)
        await channel.send("I'm Sorry. This command is disabled and it can't be used.")
    elif isinstance(error, commands.CommandInvokeError):
        channel = ctx.message.channel
        print('In {0.command.qualified_name}:'.format(ctx), file=sys.stderr)
        traceback.print_tb(error.original.__traceback__)
        print('{0.__class__.__name__}: {0}'.format(error.original), file=sys.stderr)
        e = discord.Embed(title='Inkx! I have encountered an Error!', color=0xcc6600)
        e.add_field(name='Invoke', value=error)
        e.description = '```py\nIn {0.command.qualified_name}:\n```'.format(ctx) + '{0.__class__.__name__}: {0}'.format(error.original)
        e.timestamp = datetime.datetime.utcnow()
        ch = bot.get_channel(348268312427364374)
        try:
            await ch.send(embed=e)
        except:
            pass

    elif isinstance(error, commands.CommandNotFound):
        log.info(f"\"{ctx.message.guild}\": \"{ctx.message.author}\" used a command thats not in Inkxbot, content is resent here: '{ctx.message.content}'")
    elif isinstance(error, commands.MissingRequiredArgument):
        channel = ctx.message.channel
        await channel.trigger_typing()
        await asyncio.sleep(1)
        await channel.send(f"You've asked me about my `{ctx.command}` command without arguments, use `,help {ctx.command}`")

@bot.event
async def on_error(event, *args, **kwargs):
    e = discord.Embed(title='Inkx! I have encountered an Error!', color=0xcc6600)
    e.add_field(name='Event', value=event)
    e.description = f'```py\n{traceback.format_exc()}\n```'
    e.timestamp = datetime.datetime.utcnow()
    ch = bot.get_channel(348268312427364374)
    try:
        log.info(event)
        await ch.send(embed=e)
    except:
        pass

@bot.event
async def on_resumed():
    print('resumed...')

@bot.command(hidden=True)
@commands.is_owner()
async def do(ctx, times : int, *, command):
    """Repeats a command a specified number of times."""
    msg = copy.copy(ctx.message)
    msg.content = command
    for i in range(times):
        await bot.process_commands(msg)

@bot.command(hidden=True)
@commands.is_owner()
async def shutdown(ctx):
    """Shuts down the bot: owner only"""
    await ctx.trigger_typing()
    await asyncio.sleep(1)
    await ctx.send("shutting down...")
    await bot.change_presence(game=None, status=discord.Status.invisible)
    await asyncio.sleep(1)
    await bot.close()
    os._exit(0)


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
    bot.challongekey = credentials['challongekey']
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
