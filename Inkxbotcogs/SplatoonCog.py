import asyncio
import aiohttp

import logging
import json

from discord.ext import commands
import discord

log = logging.getLogger()


def mode_key(argument):
    lower = argument.lower().strip('"')
    if lower.startswith('rank'):
        return 'Ranked Battle'
    elif lower.startswith('turf') or lower.startswith('regular'):
        return 'Regular Battle'
    elif lower == 'league':
        return 'League Battle'
    else:
        raise commands.BadArgument('Unknown schedule type, try: "ranked", "regular", or "league"')


class Splatoon:
    """Splatoon 2 related commands."""

    def __init__(self, bot):
        self.bot = bot

    async def __error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            return await ctx.send(error)

    async def load_schedule(self):
        async with self.bot.aio_session.get("https://splatoon.ink/schedule2.json") as url:
            return await url.json()

    async def alltypes_map_schedule(self, ctx, number):
        splatoonjson = await self.load_schedule()
        dict = splatoonjson
        regular = dict['modes']['regular']
        ranked  = dict['modes']['gachi']
        league  = dict['modes']['league']
        regmaps = regular[number]['maps']
        rnk = ranked[number]
        lge = league[number]
        rnkmd = rnk['rule']['name']
        lgemd = lge['rule']['name']
        rnkmaps = rnk['maps']
        lgemaps = lge['maps']
        t1 = regmaps[0]
        t2 = regmaps[1]
        r1 = rnkmaps[0]
        r2 = rnkmaps[1]
        l1 = lgemaps[0]
        l2 = lgemaps[1]
        if number == 0:
            titlename = 'Current maps in Splatoon 2'
        else:
            titlename = 'Upcoming maps in Splatoon 2'
        desc = "**Ranked Battle** \n*__{0}:__* {1} and {2} \n".format(rnkmd, r1, r2) + "**League Battle** \n*__{0}:__* {1} and {2} \n".format(lgemd, l1, l2) + "**Regular Battle** \n*__Turf War:__* {0} and {1} \n".format(t1, t2)
        sched_embed = discord.Embed(title=titlename, description=desc, color=0xFF8C00)
        await ctx.trigger_typing()
        await asyncio.sleep(1)
        await ctx.send(embed=sched_embed)

    async def modetype_splatoon2_schedule(self, ctx, mode):
        splatoonjson = await self.load_schedule()
        dict = splatoonjson
        if mode == 'Ranked Battle':
            md = 'Ranked'
            basebatt = 'gachi'
        elif mode == 'League Battle':
            md = 'League'
            basebatt = 'league'
        elif mode == 'Regular Battle':
            md = 'Regular Battle'
            basebatt = 'regular'
        else:
            log.info('something fucked up... fix it?')

        sch = dict['modes'][basebatt]
        sch1 = sch[0]
        sch2 = sch[1]
        sch3 = sch[2]
        schmd1 = sch1['rule']['name']
        schmd2 = sch2['rule']['name']
        schmd3 = sch3['rule']['name']
        sone1 = sch1['maps'][0]
        sone2 = sch1['maps'][1]
        stwo1 = sch2['maps'][0]
        stwo2 = sch2['maps'][1]
        sthr1 = sch3['maps'][0]
        sthr2 = sch3['maps'][1]
        desc = "**Current Rotation** \n*__{0}:__* {1} and {2} \n".format(schmd1, sone1, sone2) + "**Next Rotation** \n*__{0}:__* {1} and {2} \n".format(schmd2, stwo1, stwo2) + "** Next Next Rotation** \n*__{0}:__* {1} and {2} \n".format(schmd3, sthr1, sthr2)
        sched_embed = discord.Embed(title='Map Schedule for {} in Splatoon 2'.format(md), description=desc, color=0xFF8C00)
        await ctx.trigger_typing()
        await asyncio.sleep(1)
        await ctx.send(embed=sched_embed)

    @commands.command(aliases=['maps'])
    async def schedule(self, ctx, *, type: mode_key = None):
        """Shows the current Splatoon 2 schedule."""
        if type is None:
            num = 0
            await self.alltypes_map_schedule(ctx, num)
        else:
            await self.modetype_splatoon2_schedule(ctx, type)

    @commands.command()
    async def nextmaps(self, ctx):
        """Shows the next Splatoon 2 maps."""
        num = 1
        await self.alltypes_map_schedule(ctx, num)


    # I could do the Splatfest stuff later

    #@commands.command()
    #async def splatfest(self, ctx):
        #"""Shows information about the currently running NA Splatfest, if any."""
        #if self.sp2_festival is None:
            #return await ctx.send('No Splatfest has been announced.')

        #await ctx.send(embed=self.sp2_festival.embed())

def setup(bot):
    bot.add_cog(Splatoon(bot))
