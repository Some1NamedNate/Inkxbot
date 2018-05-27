import asyncio
import aiohttp
import time
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
    elif lower == 'season':
    	return 'X rank'
    else:
        raise commands.BadArgument('Unknown schedule type, try: "ranked", "season", "regular", or "league"')

def region_key(argument):
    lower = argument.lower().strip('"') 
    if lower.startswith('us') or lower.startswith('usa'):
        return 'The United States'
    elif lower.startswith('eu') or lower.startswith('europe'):
        return 'Europe'
    elif lower.startswith('jpn') or lower.startswith('japan'):
        return 'Japan'
    else:
        raise commands.BadArgument('Unknown region type, try: "usa", "europe", or "japan"')


def clouts():
    with open('mapcallouts.json') as m:
        return json.load(m)

def sr_mapredirect():
    with open('srmaps.json') as sr:
        return json.load(sr)

def map_key(argument):
    return

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

    async def load_sr(self):
        async with self.bot.aio_session.get("https://splatoon2.ink/data/coop-schedules.json") as srurl:
            return await srurl.json()

    async def load_festival(self):
        async with self.bot.aio_session.get("https://splatoon2.ink/data/festivals.json") as festurl:
            return await festurl.json()


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
        sched_embed = discord.Embed(title=titlename, description=desc, color=0x006AFF)
        sched_embed.set_footer(text="For the maps for the X rank season, do `,maps season`")
        await ctx.trigger_typing()
        await asyncio.sleep(1)
        await ctx.send(embed=sched_embed)

    async def modetype_splatoon2_schedule(self, ctx, mode):
        splatoonjson = await self.load_schedule()
        dict = splatoonjson
        if mode == 'Ranked Battle':
            md = 'Ranked'
            basebatt = 'gachi'
            co = 0xFF6F00
        elif mode == 'League Battle':
            md = 'League'
            basebatt = 'league'
            co = 0xFF004C
        elif mode == 'Regular Battle':
            md = 'Regular Battle'
            basebatt = 'regular'
            co = 0x4DFF00
        elif mode == 'X rank':
        	md = 'Xrank'
        	basebatt = 'gachi'
        	co = 0xFF6F00
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
        if md == 'Xrank':
            sched_embed = discord.Embed(title='This Season for X rank', color=co)
            sched_embed.add_field(name='Maps', value='The Reef\nHumpback Pumptrack\nInkblot Art Acadamy\nMako Mart\nWallye Warehouse\nGoby Arena\nPiranha Pit\nCamp Triggerfish')
            sched_embed.add_field(name='Modes', value=f'Current: {schmd1}\nNext: {schmd2}\nLater: {schmd3}')
        else:
        	desc = "**Current Rotation** \n*__{0}:__* {1} and {2} \n".format(schmd1, sone1, sone2) + "**Next Rotation** \n*__{0}:__* {1} and {2} \n".format(schmd2, stwo1, stwo2) + "**Next Next Rotation** \n*__{0}:__* {1} and {2} \n".format(schmd3, sthr1, sthr2)
        	sched_embed = discord.Embed(title='Map Schedule for {} in Splatoon 2'.format(md), description=desc, color=co)
        await ctx.trigger_typing()
        await asyncio.sleep(1)
        await ctx.send(embed=sched_embed)

    
    async def festival(self,ctx,region):
        if region == 'The United States':
            rg = 'na'
            basereg = 'na'
        elif region == 'Europe':
            rg = 'eu'
            basereg = 'eu'
        elif region == 'Japan':
            rg = 'jp'
            basereg = 'jp'
        else:
            log.info('something fucked up... fix it?')

        festsch = await self.load_festival()
        dict = festsch
        curtime = time.time()
        basefest = dict[rg]['festivals'][0]
        times = basefest['times']
        names = basefest['names']
        alpha = names['alpha_short']
        bravo = names['bravo_short']
        teams = alpha + " vs " + bravo
        imageurl = 'https://splatoon2.ink/assets/splatnet' + basefest['images']['panel']
        if times['result'] < curtime:
            await ctx.trigger_typing()
            await asyncio.sleep(1)
            await ctx.send("No Splatfest for " + region + " has been announced.")
        elif times['end'] < curtime:
            festemb = discord.Embed(title="The Splatfest for " + region + " is over! Results will come soon!", description=teams)
            festemb.set_image(url=imageurl)
            festemb.set_footer(text="Data obtained from splatoon2.ink")
            await ctx.trigger_typing()
            await asyncio.sleep(1)
            await ctx.send(embed=festemb)
        elif times['start'] < curtime:
            festemb = discord.Embed(title="The Ongoing Splatfest for " + region + ".", description=teams)
            festemb.set_image(url=imageurl)
            festemb.set_footer(text="Data obtained from splatoon2.ink")
            await ctx.trigger_typing()
            await asyncio.sleep(1)
            await ctx.send(embed=festemb)
        elif times['announce'] < curtime:
            festemb = discord.Embed(title="The Upcomming Splatfest for " + region + ".", description=teams)
            festemb.set_image(url=imageurl)
            festemb.set_footer(text="Data obtained from splatoon2.ink")
            await ctx.trigger_typing()
            await asyncio.sleep(1)
            await ctx.send(embed=festemb)
        else:
            await ctx.trigger_typing()
            await asyncio.sleep(1)
            await ctx.send("no splatfests are coming anymore...")

        #emb = discord.Embed(title="", description=)
        #emb.set_image(url=imageurl)
        #emb.set_footer(text="Data obtained from splatoon2.ink")


    async def sr_schedule(self,ctx,num):
        srsch = await self.load_sr()
        dict = srsch
        images = sr_mapredirect()
        basedets = dict['details'][num]
        schsrtime = basedets['start_time']
        curtime = time.time()
        stagename = basedets['stage']['name']
        imageurl = images[stagename]['map']
        weapons = basedets['weapons']
        w1 = weapons[0]
        w2 = weapons[1]
        w3 = weapons[2]
        w4 = weapons[3]

        if w1 == None:
            wep1 = 'Mystery'
        else:
            wep1 = w1['name']

        if w2 == None:
            wep2 = 'Mystery'
        else:
            wep2 = w2['name']

        if w3 == None:
            wep3 = 'Mystery'
        else:
            wep3 = w3['name']

        if w4 == None:
            wep4 = 'Mystery'
        else:
            wep4 = w4['name']

        if schsrtime > curtime:
            keyword = "Upcomming"
        else:
            keyword = "Ongoing"
        emb = discord.Embed(title=keyword+" shift for Salmon Run", description=stagename, color=0xFF8C00)
        emb.set_image(url=imageurl)
        emb.set_footer(text="Data obtained from splatoon2.ink")
        emb.add_field(name='Weapons', value=wep1+'\n'+wep2+'\n'+wep3+'\n'+wep4)
        await ctx.trigger_typing()
        await asyncio.sleep(1)
        await ctx.send(embed=emb)


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

    @commands.command(aliases=['sr'])
    async def salmon(self, ctx):
        num = 0
        await self.sr_schedule(ctx, num)

    @commands.command()
    async def nextsr(self, ctx):
        num = 1
        await self.sr_schedule(ctx, num)

    @commands.command(aliases=['c'])
    async def callouts(self, ctx, mapname):
        """Posts an image of callouts in a map of Splatoon 2, ",callouts list" for the entire list of callouts"""
        files = clouts()
        try:
            clout = files[mapname]['map']
            if clout is None:
                await ctx.trigger_typing()
                await asyncio.sleep(1)
                await ctx.send("That's nothing in my database.")
            else:
                await ctx.trigger_typing()
                await asyncio.sleep(1)
                await ctx.send(file=discord.File(clout))
    #making it an exception for ",callouts list"
        except KeyError:
            d = "reef \nfitness \nmoray \nmako \nblackbelly \ncanal \nstarfish \nhumpback \ninkblot \nmanta \nport \nsturgeon \ndome \nwalleye \narowana \nshellendorf \ngoby \npit \npitrm \ncamp"
            em = discord.Embed(title='List of Map Callouts', description=d, color=0xFF8C00)
            await ctx.trigger_typing()
            await asyncio.sleep(1)
            await ctx.send(embed=em)

    @commands.command(hidden=True)
    async def dome(self, ctx):
        await ctx.send(file=discord.File('dome.png'))

    @commands.command()
    async def splatfest(self, ctx, *, type: region_key = None):
        """Shows information about the currently running Splatfests, if any. Defaults to us."""
        if type is None:
            await self.festival(ctx,'The United States')
        else:
            await self.festival(ctx,type)

def setup(bot):
    bot.add_cog(Splatoon(bot))
