import asyncio

import discord


class Backgndtsk:
    """ a cog that creates the playing status loop """

    def __init__(self, bot):
        self.bot = bot
        self.taskupdater = bot.loop.create_task(self.background_task())

    def __unload(self):
        self.taskupdater.cancel()

    async def background_task(self):
        # this background task is for changing the playing status
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            await self.bot.change_presence(game=discord.Game(name='https://inkxbot.github.io', type=0))
            await asyncio.sleep(30)
            await self.bot.change_presence(game=discord.Game(name=',help | {} servers'.format(len(self.bot.guilds)), type=0))
            await asyncio.sleep(30)
            await self.bot.change_presence(game=discord.Game(name=',help for info', type=0))
            await asyncio.sleep(30)
            await self.bot.change_presence(game=discord.Game(name='PSnews: BREAKING NEWS!', type=0))
            await asyncio.sleep(3)
            await self.bot.change_presence(game=discord.Game(name='PSnews: SPLATOON 2 COMMANDS ARE HERE!', type=0))
            await asyncio.sleep(5)

def setup(bot):
    bot.add_cog(Backgndtsk(bot))