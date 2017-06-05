from discord.ext import commands
from .utils import config, maps
import asyncio, aiohttp
from urllib.parse import quote as urlquote
import urllib.request
import random
from collections import namedtuple
import discord
from splatoon import Client
import json


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


def load_maps():
    with open('maps.json') as m:
        return json.load(m)

def load_modes():
    with open('modes.json') as r:
        return json.load(r)

def load_schedule():
    with urllib.request.urlopen("https://splatoon.ink/schedule.json") as url:
        return json.loads(url.read().decode())

def load_cred():
    with open('splatooncred.json') as c:
        return json.load(c)

class Splatoon:
    """ Splatoon related commands. """

    def __init__(self, bot):
        self.bot = bot
        self.config = config.Config('splatoon.json', loop=bot.loop)
        self.map_data = []
        self.map_updater = self.bot.loop.create_task(self.update_maps())

    def __unload(self):
        self.map_updater.cancel()

    async def splatnet_cookie(self):
        username = self.config.get('username')
        password = self.config.get('password')
        self.cookie = await maps.get_new_splatnet_cookie(username, password)

    async def update_maps(self):
        try:
            await self.splatnet_cookie()
            while not self.bot.is_closed():
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

#    @commands.event()
#    async def loop_schedulecommand(self, ctx):


    @commands.command(aliases=['rotation'], hidden=True)
    async def maps(self, ctx):
        """Shows the current maps in the Splatoon schedule."""
        splatoonjson = load_schedule()
        dict = splatoonjson['schedule']
        current = dict[0]
        currentranked = current['ranked']
        currentmode = currentranked['rulesEN']
        crankedmaps = currentranked['maps']
        cregmaps = current['regular']['maps']
        cregone = cregmaps[0]['nameEN']
        cregtwo = cregmaps[1]['nameEN']
        crmone = crankedmaps[0]['nameEN']
        crmtwo = crankedmaps[1]['nameEN']
        desc ="**{0}:** {1} and {2} \n".format(currentmode, crmone, crmtwo) + "**Turf War:** {0} and {1}".format(cregone, cregtwo)
        mps_embed = discord.Embed(title='CURRENT ROTATION', description=desc, color=0xFF8C00)
        await ctx.trigger_typing()
        await asyncio.sleep(1)
        await ctx.send(embed=mps_embed)

    @commands.command(hidden=True)
    async def nextmaps(self, ctx):
        """Shows the next maps in the Splatoon schedule."""
        await ctx.send(self.get_map_message(1))

    @commands.command(hidden=True)
    async def lastmaps(self, ctx):
        """Shows the last maps in the Splatoon schedule."""
        await ctx.send(self.get_map_message(2))

    @commands.command(aliases=['s'])
    async def schedule(self, ctx):
        """Shows the current Splatoon schedule."""
        splatoonjson = load_schedule()
        dict = splatoonjson['schedule']
        current = dict[0]
        nex     = dict[1]
        last    = dict[2]
        currentmode = current['ranked']['rulesEN']
        crankedmaps = current['ranked']['maps']
        cregmaps = current['regular']['maps']
        cregone = cregmaps[0]['nameEN']
        cregtwo = cregmaps[1]['nameEN']
        crmone = crankedmaps[0]['nameEN']
        crmtwo = crankedmaps[1]['nameEN']
        nextmode = nex['ranked']['rulesEN']
        nrankedmaps = nex['ranked']['maps']
        nregmaps = nex['regular']['maps']
        nrmone = nrankedmaps[0]['nameEN']
        nrmtwo = nrankedmaps[1]['nameEN']
        nregone = nregmaps[0]['nameEN']
        nregtwo = nregmaps[1]['nameEN']
        descur = "**Current Rotation** \n" + "*__{0}:__* {1} and {2} \n".format(currentmode, crmone, crmtwo) + "*__Turf War:__* {0} and {1} \n".format(cregone, cregtwo)
        desnex = "**Next Rotation** \n" "*__{0}:__* {1} and {2} \n".format(nextmode, nrmone, nrmtwo) + "*__Turf War:__* {0} and {1} \n".format(nregone, nregtwo)
        desc = descur + desnex
        sched_embed = discord.Embed(title='SPLATOON SCHEDULE', description=desc, color=0xFF8C00)
        await ctx.trigger_typing()
        await asyncio.sleep(1)
        await ctx.send(embed=sched_embed)
    @commands.command(invoke_without_command=True)
    async def scrim(self, ctx, games=5, *, mode : str = None):
        """Generates scrim map and mode combinations.
        The mode combinations do not have Turf War. The number of games must
        be between 3 and 16.
        The Ranked Mode is rotated unless you pick a Ranked Mode to play, in which all map
        combinations will use that mode instead.ranked
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
                await ctx.trigger_typing()
                await asyncio.sleep(1)
                await ctx.send('Could not figure out what mode you meant.')
                return
        else:
            random.shuffle(modes)
            scrims = get_random_scrims(modes, maps, game_count)
            result = ['Game {0}: {1.mode} on {1.stage}'.format(game, scrim) for game, scrim in enumerate(scrims, 1)]
        scrim_embed = discord.Embed(title='SPLATOON SCRIM GAMES', description="{}".format("\n".join(result)), color=0xFF8C00)
        await ctx.trigger_typing()
        await asyncio.sleep(1)
        await ctx.send(embed=scrim_embed)


    @commands.command()
    async def woomy(self, ctx):
        '''Spams "Woomy!"'''
        await ctx.send('Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy!')

def setup(bot):
    bot.add_cog(Splatoon(bot))
