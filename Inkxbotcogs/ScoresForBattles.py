from discord.ext import commands
from .utils import checks
import discord
import asyncio
import json

def load_teams():
    with open('teams.json') as l:
        return json.load(l)

def load_trnynames():
    with open('tournamentnames.json') as t:
        return json.load(t)

class Scoring:
    """Commands that display scores from e-sport battles against teams."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['p'], pass_context=True, hidden=False)
    @commands.guild_only()
    @checks.mod_or_permissions()
    async def post(self, ctx, battle, homescr, args, awayscr):
        """posts a scrim score. You will need a 'Bot Commander' role in order to use this EXAMPLE: ,post 'Tournament or Scrim' 2 'name of clan you scrimed against' 1"""
        teams = load_teams()
        trnys = load_trnynames()
        guild = ctx.message.guild
        guildidstr = str(guild.id)
        teamguild = teams[guildidstr]
        teamname = teamguild['team']
        trnyname = trnys[battle]['tourny']
        try:
            if battle == 'scrim':
                channel = discord.utils.get(guild.channels, name='scrim-scores')
                await channel.send("**Scrim** \n{0} {1}  -  {3} {2}".format(teamname, homescr, args, awayscr))
                await ctx.trigger_typing()
                await asyncio.sleep(1)
                await ctx.send("done")
                return

            elif battle == battle:
                channel = discord.utils.get(guild.channels, name='tournament-scores')
                await channel.send("**Tournament**: {4} \n{0} {1}  -  {3} {2}".format(teamname, homescr, args, awayscr, trnyname))
                await ctx.trigger_typing()
                await asyncio.sleep(1)
                await ctx.send("done")
                return

            elif guildidstr not in teams:
                await ctx.trigger_typing()
                await asyncio.sleep(1)
                await ctx.send("You haven't given me your team's name, type `,writeteam \"YOUR TEAM'S NAME HERE\"` to store it into my database")
                return

            else:
                await ctx.trigger_typing()
                await asyncio.sleep(1)
                await ctx.send("It seems there's a problem, try again")
                return
        except Exception as e:
            await ctx.send("A {} has occured, plese screenshot this and send this to `InkxtheSquid#8052` on Discord".format(type(e)))
            print(e)

    @commands.command(aliases=['wt'], pass_context=True, hidden=False)
    @commands.guild_only()
    async def writeteam(self, ctx, args):
        """I will write the name of your clan to my database \n You will need a 'Bot Commander' role in order to use this"""
        guild = ctx.message.guild
        teams = load_teams()
        d = teams
        d[guild.id] = {}
        d[guild.id]["team"] = args
        await ctx.trigger_typing()
        with open('teams.json', 'w') as fp:
            json.dump(d, fp, indent=2)
        await asyncio.sleep(1)
        await ctx.send("I have successfully written your team's name into my database")

def setup(bot):
    bot.add_cog(Scoring(bot))