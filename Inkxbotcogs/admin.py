from discord.ext import commands
from .utils import checks
import discord
import inspect

# to expose to the eval command
import datetime
from collections import Counter

class Admin:
    """Admin-only commands that make the bot dynamic."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    @checks.is_owner()
    async def load(self, *, module : str):
        """Loads a module."""
        extention = "Inkxbotcogs." + module
        try:
            self.bot.load_extension(extention)
        except Exception as e:
            await self.bot.say('BAKA!')
            await self.bot.say('{}: {}'.format(type(e).__name__, e))
        else:
            await self.bot.say('All done sir')

    @commands.command(hidden=True)
    @checks.is_owner()
    async def unload(self, *, module : str):
        """Unloads a module."""
        extention = "Inkxbotcogs." + module
        try:
            self.bot.unload_extension(extention)
        except Exception as e:
            await self.bot.say('BAKA!')
            await self.bot.say('{}: {}'.format(type(e).__name__, e))
        else:
            await self.bot.say('All done sir')

    @commands.command(name='reload', hidden=True)
    @checks.is_owner()
    async def _reload(self, *, module : str):
        """Reloads a module."""
        extention = "Inkxbotcogs." + module
        try:
            self.bot.unload_extension(extention)
            self.bot.load_extension(extention)
        except Exception as e:
            await self.bot.say('BAKA!')
            await self.bot.say('{}: {}'.format(type(e).__name__, e))
        else:
            await self.bot.say('All done sir')

    @commands.command(pass_context=True, hidden=True)
    @checks.is_owner()
    async def debug(self, ctx, *, code : str):
        """Evaluates code."""
        code = code.strip('` ')
        python = '```py\n{}\n```'
        result = None

        env = {
            'bot': self.bot,
            'ctx': ctx,
            'message': ctx.message,
            'server': ctx.message.server,
            'channel': ctx.message.channel,
            'author': ctx.message.author
        }

        env.update(globals())

        try:
            result = eval(code, env)
            if inspect.isawaitable(result):
                result = await result
        except Exception as e:
            await self.bot.say(python.format(type(e).__name__ + ': ' + str(e)))
            return

        await self.bot.say(python.format(result))
        
    
    
    @commands.command(pass_context=True, hidden=True)
    @checks.is_owner()
    async def newstuff(self):
        """sends a message about a new feature in all servers"""
        await self.bot.say("All done sir")
        await self.bot.send_message(discord.Object(id='248106639410855936'), "@here, A new WordPress post about my development has been made, check it out at <https://inkxbot.wordpress.com/>")
        await self.bot.send_message(discord.Object(id='227514633735372801'), "A new WordPress post about my development has been made, check it out at <https://inkxbot.wordpress.com/>")
        await self.bot.send_message(discord.Object(id='258350226279104512'), "A new WordPress post about my development has been made, check it out at <https://inkxbot.wordpress.com/>")

def setup(bot):
    bot.add_cog(Admin(bot))
