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
        await asyncio.sleep(10)
        while not self.bot.is_closed():
            await self.bot.change_presence(activity=discord.Game(name='https://inkxbot.github.io'))
            await asyncio.sleep(60)
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='{} servers | ,help'.format(len(self.bot.guilds))))
            await asyncio.sleep(60)
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=',help for info'))
            await asyncio.sleep(60)

def setup(bot):
    bot.add_cog(Backgndtsk(bot))
