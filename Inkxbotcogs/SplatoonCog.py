import discord
from discord.ext import commands
from .utils import config, checks, maps
import asyncio, aiohttp
from urllib.parse import quote as urlquote
import random
from collections import namedtuple

GameEntry = namedtuple('GameEntry', ('stage', 'mode'))

def is_valid_entry(result, entry):
    # no dupes
    if entry in result:
        return False

    # the map can't be played in the last 2 games
    last_two_games = result[-2:]
    for prev in last_two_games:
        if prev.stage == entry.stage:
            return False

    return True

def get_random_scrims(modes, maps, count):
    result = []
    current_mode_index = 0
    for index in range(count):
        while True:
            entry = GameEntry(stage=random.choice(maps), mode=modes[current_mode_index])
            if is_valid_entry(result, entry):
                result.append(entry)
                current_mode_index += 1
                if current_mode_index >= len(modes):
                    current_mode_index = 0
                break

    return result

class Splatoon:
    """ Splatoon related commands. """

    def __init__(self, bot):
        self.bot = bot
        self.config = config.Config('splatoon.json', loop=bot.loop)
        self.map_data = []
        self.map_updater = bot.loop.create_task(self.update_maps())

    def __unload(self):
        self.map_updater.cancel()

    async def splatnet_cookie(self):
        username = self.config.get('username')
        password = self.config.get('password')
        self.cookie = await maps.get_new_splatnet_cookie(username, password)

    async def update_maps(self):
        try:
            await self.splatnet_cookie()
            while not self.bot.is_closed:
                await self.update_schedule()
                await asyncio.sleep(120) # task runs every 2 minutes
        except asyncio.CancelledError:
            pass

    async def update_schedule(self):
        try:
            schedule = await maps.get_splatnet_schedule(self.cookie)
        except:
            # if we get an exception, keep the old data
            # make sure to remove the old data that already ended
            self.map_data = [data for data in self.map_data if not data.is_over]
        else:
            self.map_data = []
            for entry in schedule:
                if entry.is_over:
                    continue
                self.map_data.append(entry)

    def get_map_message(self, index):
        try:
            return str(self.map_data[index])
        except IndexError:
            return 'No map data found. Try again later.'

#    @commands.event()
#    async def loop_schedulecommand(self):

    @commands.command(hidden=True)
    async def refreshmaps(self):
        """Force refresh the maps in the rotation."""
        await self.update_schedule()
        await self.bot.say('refreshed')

    @commands.command(pass_context=True, aliases=['rotation'])
    async def maps(self, ctx):
        """Shows the current maps in the Splatoon schedule."""
        mps_embed = discord.Embed(title='SPLATOON SCHEDULE', description="{}".format(self.get_map_message(0)), color=0xFF8C00)
        typetochan = ctx.message.channel
        await self.bot.send_typing(typetochan)
        await asyncio.sleep(1)
        await self.bot.say(embed=mps_embed)

    @commands.command(hidden=True)
    async def nextmaps(self):
        """Shows the next maps in the Splatoon schedule."""
        await self.bot.say(self.get_map_message(1))

    @commands.command(hidden=True)
    async def lastmaps(self):
        """Shows the last maps in the Splatoon schedule."""
        await self.bot.say(self.get_map_message(2))

    @commands.command(pass_context=True, aliases=['s'])
    async def schedule(self, ctx):
        """Shows the current Splatoon schedule."""
        sched_embed = discord.Embed(title='SPLATOON SCHEDULE', description="{}".format('\n'.join(map(str, self.map_data))), color=0xFF8C00)
        typetochan = ctx.message.channel
        if self.map_data:
            await self.bot.send_typing(typetochan)
            await asyncio.sleep(1)
            await self.bot.say(embed=sched_embed)
        else:
            await self.bot.send_typing(typetochan)
            await asyncio.sleep(1)
            await self.bot.say('No map data found. Try again later.')

    @commands.command(hidden=True, pass_context=True)
    async def woomy(self):
        await self.bot.say('Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy!')

    @commands.command(invoke_without_command=True, pass_context=True)
    async def scrim(self, ctx, games=5, *, mode : str = None):
        """Generates scrim map and mode combinations.
        The mode combinations do not have Turf War. The number of games must
        be between 3 and 16.
        The Ranked Mode is rotated unless you pick a Ranked Mode to play, in which all map
        combinations will use that mode instead.
        """

        maps = self.config.get('maps', [])
        modes = ['RM', 'SZ', 'TC']
        game_count = max(min(games, 16), 3)

        if mode is not None:
            mode = mode.lower()

            lookup = {
                'tc': modes[2],
                'tower': modes[2],
                'tower control': modes[2],
                'sz': modes[1],
                'zones': modes[1],
                'zone': modes[1],
                'splat zone': modes[1],
                'splat zones': modes[1],
                'rainmaker': modes[0],
                'rm': modes[0],
                'turf': 'Turf War',
                'turf war': 'Turf War',
                'tw': 'Turf War'
            }

            resulting_mode = lookup.get(mode, None)
            if resulting_mode is not None:
                result = ['The following games will be played in {}'.format(resulting_mode)]
                for index, stage in enumerate(random.sample(maps, game_count), 1):
                    result.append('Game {}: {}'.format(index, stage))
            else:
                await self.bot.send_typing(ctx.message.channel)
                await asyncio.sleep(1)
                await self.bot.say('Could not figure out what mode you meant.')
                return
        else:
            random.shuffle(modes)
            scrims = get_random_scrims(modes, maps, game_count)
            result = ['Game {0}: {1.mode} on {1.stage}'.format(game, scrim) for game, scrim in enumerate(scrims, 1)]
        scrim_embed = discord.Embed(title='SPLATOON SCRIM GAMES', description="{}".format("\n".join(result)), color=0xFF8C00)
        await self.bot.send_typing(ctx.message.channel)
        await asyncio.sleep(1)
        await self.bot.say(embed=scrim_embed)

    @commands.command(hidden=True, pass_context=True)
    @checks.is_owner()
    async def flounder(self, ctx):
        channel = ctx.message.channel
        await self.bot.send_typing(channel)
        await asyncio.sleep(1)
        await self.bot.send_file(channel, 'flounder.png')

    @commands.command(hidden=True, pass_context=True)
    @checks.is_owner()
    async def piranha(self, ctx):
        channel = ctx.message.channel
        await self.bot.send_typing(channel)
        await asyncio.sleep(1)
        await self.bot.send_file(channel, 'piranha.png')

    @commands.command(hidden=True, pass_context=True)
    @checks.is_owner()
    async def hammerhead(self, ctx):
        channel = ctx.message.channel
        await self.bot.send_typing(channel)
        await asyncio.sleep(1)
        await self.bot.send_file(channel, 'hammerhead.png')

    @commands.command(hidden=True, pass_context=True)
    @checks.is_owner()
    async def triggerfish(self, ctx):
        channel = ctx.message.channel
        await self.bot.send_typing(channel)
        await asyncio.sleep(1)
        await self.bot.send_file(channel, 'triggerfish.png')

    @commands.command(hidden=True, pass_context=True)
    @checks.is_owner()
    async def bluefin(self, ctx):
        channel = ctx.message.channel
        await self.bot.send_typing(channel)
        await asyncio.sleep(1)
        await self.bot.send_file(channel, 'bluefin.png')

    @commands.command(hidden=True, pass_context=True)
    @checks.is_owner()
    async def moray(self, ctx):
        channel = ctx.message.channel
        await self.bot.send_typing(channel)
        await asyncio.sleep(1)
        await self.bot.send_file(channel, 'moray.png')

    @commands.command(hidden=True, pass_context=True)
    @checks.is_owner()
    async def walleye(self, ctx):
        channel = ctx.message.channel
        await self.bot.send_typing(channel)
        await asyncio.sleep(1)
        await self.bot.send_file(channel, 'walleye.png')

    @commands.command(hidden=True, pass_context=True)
    @checks.is_owner()
    async def mackerel(self, ctx):
        channel = ctx.message.channel
        await self.bot.send_typing(channel)
        await asyncio.sleep(1)
        await self.bot.send_file(channel, 'mackerel.png')

    @commands.command(hidden=True, pass_context=True)
    @checks.is_owner()
    async def kelp(self, ctx):
        channel = ctx.message.channel
        await self.bot.send_typing(channel)
        await asyncio.sleep(1)
        await self.bot.send_file(channel, 'kelp.png')

    @commands.command(hidden=True, pass_context=True)
    @checks.is_owner()
    async def museum(self, ctx):
        channel = ctx.message.channel
        await self.bot.send_typing(channel)
        await asyncio.sleep(1)
        await self.bot.send_file(channel, 'museum.png')

    @commands.command(hidden=True, pass_context=True)
    @checks.is_owner()
    async def arowana(self, ctx):
        channel = ctx.message.channel
        await self.bot.send_typing(channel)
        await asyncio.sleep(1)
        await self.bot.send_file(channel, 'arowana.png')

    @commands.command(hidden=True, pass_context=True)
    @checks.is_owner()
    async def urchin(self, ctx):
        channel = ctx.message.channel
        await self.bot.send_typing(channel)
        await asyncio.sleep(1)
        await self.bot.send_file(channel, 'urchin.png')

    @commands.command(hidden=True, pass_context=True)
    @checks.is_owner()
    async def saltspray(self, ctx):
        channel = ctx.message.channel
        await self.bot.send_typing(channel)
        await asyncio.sleep(1)
        await self.bot.send_file(channel, 'saltspray.png')

    @commands.command(hidden=True, pass_context=True)
    @checks.is_owner()
    async def mahimahi(self, ctx):
        channel = ctx.message.channel
        await self.bot.send_typing(channel)
        await asyncio.sleep(1)
        await self.bot.send_file(channel, 'mahimahi.png')

    @commands.command(hidden=True, pass_context=True)
    @checks.is_owner()
    async def anchov(self, ctx):
        channel = ctx.message.channel
        await self.bot.send_typing(channel)
        await asyncio.sleep(1)
        await self.bot.send_file(channel, 'anchov.png')

    @commands.command(hidden=True, pass_context=True)
    @checks.is_owner()
    async def blackbelly(self, ctx):
        channel = ctx.message.channel
        await self.bot.send_typing(channel)
        await asyncio.sleep(1)
        await self.bot.send_file(channel, 'blackbelly.png')

def setup(bot):
    bot.add_cog(Splatoon(bot))
