import asyncio
import aiohttp
import io
import image
import json

from discord.ext import commands
import cairosvg

import challonge
import discord


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
    @commands.guild_only()
    async def bracket(self, ctx):
        """Shows a Challonge tournament bracket"""
        guild = ctx.message.guild
        challongeurls = load_challonge_urls()
        await ctx.trigger_typing()
        await asyncio.sleep(1)
        guildstr = str(guild.id)
        site = challongeurls[guildstr]["url"]
        await asyncio.sleep(1)
        try:
            cairosvg.svg2png(url=site, write_to='bracket.png')
            await asyncio.sleep(1)
            await ctx.trigger_typing()
            await ctx.send(file=discord.File("bracket.png"))
        except KeyError:
            await ctx.trigger_typing()
            await ctx.send("I don't think you've given me your chollonge bracket yet...write it to my database with `,setbracket '(challonge tournament link).svg'`")

    @commands.command(aliases=['setb'])
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def setbracket(self, ctx, args):
        """this writes your challonge url to my database.
    You must have permissions to manage channels  in order to use this"""
        guild = ctx.message.guild
        urls = load_challonge_urls()
        d = urls
        d[guild.id] = {}
        d[guild.id]["url"] = args
        await ctx.trigger_typing()
        with open('challongeurls.json', 'w') as fp:
            json.dump(d, fp, indent=2)
            await asyncio.sleep(1)
            await ctx.send("I have successfully written your current challonge bracket to my database.")

def setup(bot):
    bot.add_cog(Challonge(bot))
