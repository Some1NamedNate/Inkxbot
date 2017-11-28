import asyncio
import random
import os

from discord.ext import commands
import discord


class Easter_Eggs:
    """These commands are just for fun, they all might be removed someday"""

    def __init__(self, bot):
        self.bot = bot


    @commands.command(pass_context=True, hidden=True)
    async def e(self, ctx):
        """Shows the Easter Egg list"""
        await ctx.send("`Easter Egg list` \n" + ",cryo - Cryo Mode \n" + ",mgs - Metal Gear Mode \n" + ",falconmode - Falcon Mode \n" + ",hadoken - Ryu Mode \n" + ",baka - baka mode \n")

    @commands.command(pass_context=True, hidden=True)
    async def mgs(self, ctx):
        """An easter egg from Metal Gear Solid"""
        await ctx.trigger_typing()
        await asyncio.sleep(1)
        await ctx.send("\U0001f3b5" + "Standing... On the Edge!")

    @commands.command(pass_context=True, hidden=True)
    async def falconmode(self, ctx):
        """An easter egg referencing Captain Falcon"""
        await ctx.trigger_typing()
        await asyncio.sleep(1)
        await ctx.send("Inkxbot... PUNCH!")

    @commands.command(pass_context=True, hidden=True)
    async def cryo(self, ctx):
        """An easter egg referencing Cryo"""
        await ctx.trigger_typing()
        await asyncio.sleep(1)
        await ctx.send("PEW PEW PEW! PEW PEW PEW PEW PEW! SHUT THE F##K UP")

    @commands.command(pass_context=True, hidden=True)
    async def hadoken(self, ctx):
        """An easter egg from Street Fighter"""
        await ctx.trigger_typing()
        await asyncio.sleep(1)
        await ctx.send("**HADOKEN!**")

    @commands.command(pass_context=True, hidden=True)
    async def baka(self, ctx):
        """BAKA"""
        await ctx.trigger_typing()
        randombaka = random.choice(os.listdir('bakas/'))
        await asyncio.sleep(1)
        await ctx.send(file=discord.File('bakas/' + randombaka))

    @commands.command(pass_context=True, hidden=True)
    async def woomy(self, ctx):
        """woomy!"""
        await ctx.trigger_typing()
        await ctx.send('WOOMY! WOOMY! WOOMY! WOOMY! WOOMY! WOOMY! WOOMY! WOOMY! WOOMY! WOOMY! WOOMY! WOOMY! WOOMY! WOOMY! WOOMY! WOOMY! WOOMY! WOOMY! WOOMY! WOOMY! WOOMY! WOOMY! WOOMY! WOOMY! WOOMY! WOOMY! WOOMY!')

    @commands.command(pass_context=True, hidden=True)
    async def baguette(self, ctx):
        """baguette"""
        await ctx.trigger_typing()
        await ctx.send('<:foxbot:244929610146381824><:mademe:244929610792304640><:dothis:244929610607886337>')

    @commands.command(pass_context=True, hidden=True)
    async def muda(self, ctx):
        """muda!"""
        await ctx.trigger_typing()
        await ctx.send('MUDA! MUDA! MUDA! MUDA! MUDA! MUDA! MUDA! MUDA! MUDA! MUDA! MUDA! MUDA! MUDA! MUDA! MUDA! MUDA! MUDA! MUDA! MUDA! MUDA! MUDA! MUDA! MUDA! MUDA! MUDA! MUDA! MUDA! MUDA! MUDA! MUDA! MUDA! MUDA! MUDA!')

    @commands.command(pass_context=True, hidden=True)
    async def spacecore(self, ctx):
        """spaaaaaaaaaaaace!"""
        await ctx.trigger_typing()
        await ctx.send('SPAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACE!!1!')
        
def setup(bot):
    bot.add_cog(Easter_Eggs(bot))
