import discord;
from discord.ext import commands
from .utils import config, checks
import asyncio

class Moderation:
    """ Moderative Commands to keep the server clean """

    def __init__(self, bot):
        self.bot = bot
    #def is_me(m):
    #    return m.author == client.user

    #deleted = await client.purge_from(channel, limit=100, check=is_me)
    #await client.send_message(channel, 'Deleted {} message(s)'.format(len(deleted)))
    
    
    @commands.command(pass_context=True, no_pm=True, name = 'clear')
    @commands.has_role('Bot Commander')
    async def _clear(self, ctx, amount : int = 100):
        """Deletes my messages."""
		
        channel = ctx.message.channel

        calls = 0;
        async for msg in self.bot.logs_from(channel, limit=amount, before=ctx.message):
            if calls and calls % 5 == 0:
                await asyncio.sleep(1.5)

            if msg.author == self.bot.user:
                await self.bot.delete_message(msg)
                calls += 1
        await self.bot.say('Deleted {0}'.format(calls))
        await asyncio.sleep(1.5)
        await self.bot.delete_message(channel, limit=1, after=ctx.message)
        
    @commands.command(pass_context=True, no_pm=True)
    @commands.has_role('Bot Commander')
    async def purge(self, ctx, amount : int = 5):
        """Deletes specified number of messages."""
        await self.bot.purge_from(ctx.message.channel, limit=amount, before=ctx.message)
        await self.bot.say('Deleted {0}'.format(amount))
        await asyncio.sleep(1.5)
        #await self.bot.delete_message(ctx.message.channel, limit=, after=ctx.message)

#    the command below is still in development. I'm sorry if the development is gonna take long
    
#    @commands.command(pass_context=True, no_pm=True)
#    @commands.has_role('Bot Commander')
#    async def give(self, ):
#        """Gives a role to a user"""

def setup(bot):
    bot.add_cog(Moderation(bot))
