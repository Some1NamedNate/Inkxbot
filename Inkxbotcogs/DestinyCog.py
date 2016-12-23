from discord.ext import commands
from .utils import config, checks#, hcards
import asyncio, aiohttp
from urllib.parse import quote as urlquote
from collections import namedtuple
import requests

class Destiny:
    def __init__(self, bot):
        self.bot = bot     
        #self.loop = AbstractEventLoop.run_in_executor()         

    @commands.command()
    async def deswiki(self, title):
        """Returns a Destinypedia page. For spaces use underscores."""
        url = 'http://destiny.wikia.com/wiki/' + urlquote(title)

        async with aiohttp.get(url) as resp:
            if resp.status == 404:
                await self.bot.say('Could not find your page. Try a search:\n{0.url}'.format(resp))
            elif resp.status == 200:
                await self.bot.say(resp.url)
            elif resp.status == 502:
                await self.bot.say('Seems like the Destinypedia is taking too long to respond. Try again later.')
            else:
                await self.bot.say('An error has occurred of status code {0.status} has happened. Tell Inkx.'.format(resp))

def setup(bot):
    bot.add_cog(Destiny(bot))
