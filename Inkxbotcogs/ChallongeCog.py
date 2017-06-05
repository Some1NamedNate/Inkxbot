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
        guild = channel.guild # I hope this works
        guildstr = str(guild.id)
        while not self.bot.is_closed():
            guildchallonge = challongeurls[guildstr]
            url = guildchallonge["url"]
            tournament = challonge.tournaments.show(url)
            participants = challonge.participants.index(tournament["id"])
            number = len(participants)
            name = (tournament["name"])
            signup = (tournament["sign-up-url"])
            await channel.send("**{1}** \n teams/players participating in this tournament: {0} \n signup link: {2}".format(number, name, signup))
            await asyncio.sleep(1800) #runs every 30 mins

    @commands.command()
    async def bracket(self, ctx):
        """Shows a Challonge tournament bracket"""
        guild = ctx.message.guild
        challongeurls = load_challonge_urls()
        guildstr = str(guild.id)
        site = challongeurls[guildstr]["url"]
        tournament = challonge.tournaments.show(site)
        await ctx.trigger_typing()
        img = (tournament["live-image-url"])
        driver = webdriver.PhantomJS()
        driver.maximize_window()
        driver.get(img)
        driver.save_screenshot('bracket.png')
        await ctx.send(file=discord.File('bracket.png'))

    @commands.command(aliases=['setid'])
    @checks.TO_or_permissions()
    async def seturl(self, ctx, args):
        """this writes your challonge url to my database.
        ask in Inkxbot's server for help"""
        guild = ctx.message.guild
        urls = load_challonge_urls()
        d = urls
        d[guild.id] = {}
        d[guild.id]["url"] = args
        await ctx.trigger_typing()
        with open('challongeurls.json', 'w') as fp:
            json.dump(d, fp, indent=2)
        await asyncio.sleep(1)
        await ctx.send("I have successfully written your current challonge url to my database")

def setup(bot):
    bot.add_cog(Challonge(bot))