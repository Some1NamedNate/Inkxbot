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
        carbon_payload = {
            'key': self.bot.carbon_key,
            'servercount': len(self.bot.guilds)
        }

        async with self.ses sion.post(CARBONAPIBOTDATA, data=carbon_payload) as resp:
            log.info('Carbon statistics returned {0.status} for {1}'.format(resp, carbon_payload))

        payload = json.dumps({
            'server_count': len(self.bot.guilds)
        })

        headers = {
            'authorization': self.bot.dbots_key,
            'content-type': 'application/json'
        }

        url = '{0}/bots/245648163837444097/stats'.format(DBOTSAPI)
        async with self.session.post(url, data=payload, headers=headers) as resp:
            log.info('DBots statistics returned {0.status} for {1}'.format(resp, payload))


        dlpayload = {
            "token": self.bot.discordlist_token,
            "servers": len(self.bot.guilds)
        }

        serverdata = {
            "servers": len(self.bot.guilds)
        }

        dlisturl = "https://bots.discordlist.net/api.php"
        async with self.session.post(dlisturl, data=dlpayload) as resp:
            log.info('DiscordList statistics returned {0.status} for {1}'.format(resp, dlpayload))

    async def on_guild_join(self, guild):
        await guild.send("Thank you for adding me to your server! I'll be a plessure to help with many things for you! type `,help` for information on my commands!")
        await self.update()

    async def on_guild_remove(self, guild):
        await self.update()

    async def on_ready(self):
        await self.update()

def setup(bot):
    bot.add_cog(Discordlist(bot))
