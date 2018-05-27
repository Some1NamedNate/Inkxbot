# -*- coding: utf-8 -*-

from discord.ext import commands
import discord

class Adminbackup:
    """Backup Admin commands."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True, pass_context=True)
    @commands.is_owner()
    async def bkload(self, ctx, *, module : str):
        """Loads a module."""
        extention = "cogs." + module
        try:
            self.bot.load_extension(extention)
        except Exception as e:
            await ctx.send('\U0001f6ab')
            await ctx.send('{}: {}'.format(type(e).__name__, e))
        else:
            await ctx.send('<:radithumbsup:317056486297829386>')

    @commands.command(hidden=True, pass_context=True)
    @commands.is_owner()
    async def bkunload(self, ctx, *, module : str):
        """Unloads a module."""
        extention = "cogs." + module
        try:
            self.bot.unload_extension(extention)
        except Exception as e:
            await ctx.send('\U0001f6ab')
            await ctx.send('{}: {}'.format(type(e).__name__, e))
        else:
            await ctx.send('<:radithumbsup:317056486297829386>')

    @commands.command(name='bkreload', hidden=True, pass_context=True)
    @commands.is_owner()
    async def _reload(self, ctx, *, module : str):
        """Reloads a module."""
        extention = "cogs." + module
        try:
            self.bot.unload_extension(extention)
            self.bot.load_extension(extention)
        except Exception as e:
            await ctx.send('\U0001f6ab')
            await ctx.send('{}: {}'.format(type(e).__name__, e))
        else:
            await ctx.send('<:radithumbsup:317056486297829386>')

def setup(bot):
    bot.add_cog(Adminbackup(bot))
