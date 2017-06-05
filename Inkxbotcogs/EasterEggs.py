from discord.ext import commands
import asyncio
import discord

class Easter_Eggs:
    """these commands are just for fun, they all might be removed someday"""

    def __init__(self, bot):
        self.bot = bot


    @commands.command(pass_context=True, hidden=True)
    async def e(self, ctx):
        """Shows the Easter Egg list"""
        await ctx.send("`Easter Egg list` \n" + ",cyro - Cyro Mode \n" + ",mgs - Metal Gear Mode \n" + ",falconmode - Falcon Mode \n" + ",hadoken - Ryu Mode \n")

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




def setup(bot):
    bot.add_cog(Easter_Eggs(bot))