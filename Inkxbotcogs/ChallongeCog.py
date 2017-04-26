from selenium import webdriver
from discord.ext import commands
from .utils import checks
import asyncio
import discord
import challonge
import json

def load_challonge_urls():
    with open('challongeurls.json') as c:
        return json.load(c)

class Challonge:
    """ Commands that are used from Challonge. """

    def __init__(self, bot):
        self.bot = bot
        self.taskupdater = bot.loop.create_task(self.challonge_background_task())

    def __unload(self):
        self.taskupdater.cancel()

    async def challonge_background_task(self):
        # this background task is for showing updates from your tournament
        await self.bot.wait_until_ready()
        challonge.set_credentials("InkxtheSquid", self.bot.challongekey)
        challongeurls = load_challonge_urls()
        channel = discord.utils.get(self.bot.get_all_channels(), name='tournyupdates')
        server = channel.server # I hope this works
        while not self.bot.is_closed:
            url = challongeurls[server.id]["url"]
            tournament = challonge.tournaments.show(url)
            participants = challonge.participants.index(tournament["id"])
            number = len(participants)
            name = (tournament["name"])
            signup = (tournament["sign-up-url"])
            await self.bot.send_message(channel, "**{1}** \n teams/players participating in this tournament: {0} \n signup link: {2}".format(number, name, signup))
            await asyncio.sleep(1800) #runs every 30 mins

    @commands.command(pass_context=True)
    async def bracket(self, ctx, args):
        """Shows a Challonge tournament bracket: ,bracket 'Challonge link'"""
        channel = ctx.message.channel
        await self.bot.send_typing(channel)
        site = args + '.svg'
        driver = webdriver.PhantomJS()
        driver.maximize_window()
        driver.get(site)
        driver.save_screenshot('bracket.png')
        await self.bot.send_file(channel, 'bracket.png')

    @commands.command(pass_context=True)
    @checks.TO_or_permissions(manage_server=True)
    async def seturl(self, ctx, args):
        """this writes your challonge url to my database. ask in Inkxbot's server for help"""
        server = ctx.message.server
        urls = load_challonge_urls()
        d = urls
        d[server.id] = {}
        d[server.id]["url"] = args
        typetochan = ctx.message.channel
        await self.bot.send_typing(typetochan)
        with open('challongeurls.json', 'w') as fp:
            json.dump(d, fp, indent=2)
        await asyncio.sleep(1)
        await self.bot.say("I have successfully written your current challonge url to my database")

def setup(bot):
    bot.add_cog(Challonge(bot))