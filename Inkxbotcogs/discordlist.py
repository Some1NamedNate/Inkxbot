import aiohttp
import json
import logging

log = logging.getLogger()

DISCORDLIST_API = 'https://bots.discordlist.net/api'

class Discordlist:
    """Cog for updating discordlist.net bot information."""
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()

    def __unload(self):
        # pray it closes
        self.bot.loop.create_task(self.session.close())

    async def update(self):
        payload = {
            "token": '(bots token goes here)',
            "servers": len(self.bot.servers)
        }
        url = "https://bots.discordlist.net/api.php"
        resp = await aiohttp.post(url, data=payload)
        resp.close()
        async with self.session.post(url, data=payload) as resp:
            log.info('DiscordList statistics returned {0.status} for {1}'.format(resp, payload))

    async def on_server_join(self, server):
        await self.update()

    async def on_server_remove(self, server):
        await self.update()

    async def on_ready(self):
        await self.update()

def setup(bot):
    bot.add_cog(Discordlist(bot))
