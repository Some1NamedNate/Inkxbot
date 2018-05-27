from discord.ext import commands
import aiohttp
import asyncio

class Destiny:
    def __init__(self, bot):
        self.bot = bot
        #self.loop = AbstractEventLoop.run_in_executor()

    @commands.command(pass_context=True)
    async def deswiki(self, ctx, title):
        """Returns a Destinypedia page: ,deswiki 'Ghost'"""
        url = 'http://destiny.wikia.com/wiki/' + title
        async with self.bot.aio_session.get(url) as resp:
            if resp.status == 404:
                await ctx.trigger_typing()
                await asyncio.sleep(1)
                await ctx.send('Could not find your page. Try a search:\n{0.url}'.format(resp))
            elif resp.status == 200:
                await ctx.trigger_typing()
                await asyncio.sleep(1)
                await ctx.send(resp.url)
            elif resp.status == 502:
                await ctx.trigger_typing()
                await asyncio.sleep(1)
                await ctx.send('Seems like the Destinypedia is taking too long to respond. Try again later.')
            else:
                await ctx.trigger_typing()
                await asyncio.sleep(1)
                await ctx.send('An error has occurred of status code {0.status} happened. Tell Inkx.'.format(resp))

def setup(bot):
    bot.add_cog(Destiny(bot))