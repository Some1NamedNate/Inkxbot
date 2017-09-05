from discord.ext import commands

import datetime
import random
import urllib
import asyncio
import discord
import logging
import aiohttp
import yarl
import json
import re


def load_schedule():
    with urllib.request.urlopen("https://splapi2.stat.ink/schedule") as url:
        return json.loads(url.read().decode())

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
    """Splatoon related commands."""

    def __init__(self, bot):
        self.bot = bot

    async def __error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            return await ctx.send(error)

    async def alltypes_map_schedule(self, ctx, number):
        splatoonjson = load_schedule()
        dict = splatoonjson
        regular = dict['regular']
        ranked  = dict['gachi']
        league  = dict['league']
        regmaps = regular[number]['stages']
        rnk = ranked[number]
        lge = league[number]
        rnkmd = rnk['mode']['name']['en-US']
        lgemd = lge['mode']['name']['en-US']
        rnkmaps = rnk['stages']
        lgemaps = lge['stages']
        t1 = regmaps[0]['name']['en-US']
        t2 = regmaps[1]['name']['en-US']
        r1 = rnkmaps[0]['name']['en-US']
        r2 = rnkmaps[1]['name']['en-US']
        l1 = lgemaps[0]['name']['en-US']
        l2 = lgemaps[1]['name']['en-US']
        if number == 0:
            titlename = 'Current maps in Splatoon 2'
        else:
            titlename = 'Upcoming maps in Splatoon 2'
        desc = "**Ranked Battle** \n*__{0}:__* {1} and {2} \n".format(rnkmd, r1, r2) + "**League Battle** \n*__{0}:__* {1} and {2} \n".format(lgemd, l1, l2) + "**Regualar Battle** \n*__Turf War:__* {0} and {1} \n".format(t1, t2)
        sched_embed = discord.Embed(title=titlename, description=desc, color=0xFF8C00)
        await ctx.trigger_typing()
        await asyncio.sleep(1)
        await ctx.send(embed=sched_embed)

    #async def modetype_splatoon2_schedule(self, ctx, mode):
        #sched_embed = discord.Embed(title='Current maps in Splatoon 2', description=desc, color=0xFF8C00)
        #await ctx.trigger_typing()
        #await asyncio.sleep(1)
        #await ctx.send(embed=sched_embed)

    @commands.command(aliases=['maps'])
    async def schedule(self, ctx, *, type: mode_key = None):
        """Shows the current Splatoon 2 schedule."""
        if type is None:
            num = 0
            await self.alltypes_map_schedule(ctx, num)
        else:
            await ctx.send("this isn't ready yet...")
            #await self.modetype_splatoon2_schedule(ctx, type)

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
