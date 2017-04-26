import aiohttp
import json
import logging
import discord


log = logging.getLogger()

DISCORDLISTAPI   = 'https://bots.discordlist.net/api.php'
CARBONAPIBOTDATA = 'https://www.carbonitex.net/discord/data/botdata.php'
DBOTSAPI         = 'https://bots.discord.pw/api'

class Discordlist:
    """Cog for updating bot information on botlisting websites."""
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()

    def __unload(self):
        # give me hope
        self.bot.loop.create_task(self.session.close())

    async def update(self):
        # Matt hasn't given me a key yet
    #    carbon_payload = {
            #'key': self.bot.carbon_key,
            #'servercount': len(self.bot.servers)
        #}

        #async with self.ses sion.post(CARBONAPIBOTDATA, data=carbon_payload) as resp:
            #log.info('Carbon statistics returned {0.status} for {1}'.format(resp, carbon_payload))

        payload = json.dumps({
            'server_count': len(self.bot.servers)
        })

        headers = {
            'authorization': self.bot.dbots_key,
            'content-type': 'application/json'
        }

        url = '{0}/bots/{1.user.id}/stats'.format(DBOTSAPI, self.bot)
        async with self.session.post(url, data=payload, headers=headers) as resp:
            log.info('DBots statistics returned {0.status} for {1}'.format(resp, payload))


        dlpayload = {
            "token": self.bot.discordlist_token,
            "servers": len(self.bot.servers)
        }

        serverdata = {
            "servers": len(self.bot.servers)
        }

        url = "https://bots.discordlist.net/api.php"
        resp = await aiohttp.post(url, data=dlpayload)
        resp.close()
        async with self.session.post(url, data=dlpayload) as resp:
            log.info('DiscordList statistics returned {0.status} for {1}'.format(resp, serverdata))

    async def on_server_join(self, server):
        await self.bot.send_message(server, "Thank you for adding me to your server! I'll be a plessure to help with many things for you! type `,help` for information on my commands!")
        await self.update()

    async def on_server_remove(self, server):
        await self.update()

    async def on_ready(self):
        await self.update()

def setup(bot):
    bot.add_cog(Discordlist(bot))
