from selenium import webdriver
from discord.ext import commands
import asyncio
import discord

class Challonge:
    """ Commands that are used from Challonge. """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def bracket(self, ctx, args):
        """Shows the bracket of your tournament on Callonge. /nExample: ,bracket 'Challonge link'"""
        channel = ctx.message.channel
        await self.bot.send_typing(channel)
        site = args + '.svg'
        driver = webdriver.PhantomJS()
        driver.maximize_window()
        driver.get(site)
        driver.save_screenshot('bracket.png')
        channel = ctx.message.channel
        await self.bot.send_file(channel, 'bracket.png')

def setup(bot):
    bot.add_cog(Challonge(bot))
