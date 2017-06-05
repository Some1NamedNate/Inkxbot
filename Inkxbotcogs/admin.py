from discord.ext import commands
from .utils import checksre
import discord
import inspect

# to expose to the eval command
import datetime
from collections import Counter

class Admin:
    """Admin-only commands that make the bot dynamic."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True, pass_context=True)
    @commands.is_owner()
    async def load(self, ctx, *, module : str):
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
    async def unload(self, ctx, *, module : str):
        """Unloads a module."""
        extention = "cogs." + module
        try:
            self.bot.unload_extension(extention)
        except Exception as e:
            await ctx.send('\U0001f6ab')
            await ctx.send('{}: {}'.format(type(e).__name__, e))
        else:
            await ctx.send('<:radithumbsup:317056486297829386>')

    @commands.command(name='reload', hidden=True, pass_context=True)
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

    @commands.command(name = 'clean')
    @commands.is_owner()
    async def clean(self, amount : int = 100):
        """Deletes my messages.
        You will need a 'Bot Commander' role in order to use this"""

        calls = 0;
        async for msg in channel.history(limit=amount, before=ctx.message):
            if calls and calls % 5 == 0:
                await asyncio.sleep(1.5)

            if msg.author == self.bot.user:
                await ctx.delete(msg)
                calls += 1
        await ctx.send('Deleted {0}'.format(calls), delete_after=3.0)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def debug(self, ctx, *, code : str):
        """Evaluates code."""
        code = code.strip('` ')
        python = '```py\n{}\n```'
        result = None

        env = {
            'inkxbot': self.bot,
            'ctx': ctx,
            'message': ctx.message,
            'guild': ctx.message.guild,
            'channel': ctx.message.channel,
            'author': ctx.message.author
        }

        env.update(globals())

        try:
            result = eval(code, env)
            if inspect.isawaitable(result):
                result = await result
        except Exception as e:
            await ctx.send('<:radithink:316999358333714432>' + python.format(type(e).__name__ + ': ' + str(e)))
            return

        await ctx.send('<:radithink:316999358333714432>' + python.format(result))


def setup(bot):
    bot.add_cog(Admin(bot))
