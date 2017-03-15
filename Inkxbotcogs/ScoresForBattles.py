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

    @commands.command(aliases=['p'], pass_context=True, no_pm=True, hidden=False)
    @checks.mod_or_permissions()
    async def post(self, ctx, battle, homescr, args, awayscr):
        """posts a scrim score in a #scrim-scores channel \n You will need a 'Bot Commander' role in order to use this \n EXAMPLE: ,post 'Tournament or Scrim' 2 'name of clan you scrimed against' 1"""
        teams = load_teams()
        trnys = load_trnynames()
        if battle == 'scrim':
            battle = 'Scrim'
        else:
            battle = battle
        server = ctx.message.server
        teamserver = teams[server.id]
        teamname = teams[server.id]['team']
        trnyname = trnys[battle]['tourny']
        for s in server.channels:
            if battle == 'Scrim':
                if s.name == "scrim-scores":
                    await self.bot.send_message(s, "**{4}** \n{0} {1}  -  {3} {2}".format(teamname, homescr, args, awayscr, battle))
                    await self.bot.say("done")
                    break
            elif battle == battle:
                if s.name == "tournament-scores":
                    await self.bot.send_message(s, "**Tournament**: {4} \n{0} {1}  -  {3} {2}".format(teamname, homescr, args, awayscr, trnyname))
                    await self.bot.say("done")
                    break

            elif server.id not in teams:
                await self.bot.say("You haven't given me your team's name, type `,writeteam \"YOUR TEAM'S NAME HERE\"` to store it into my database")
                break

        else:
            await self.bot.say("It seems there's a problem, try again")

    @commands.command(aliases=['wt'], pass_context=True, no_pm=True, hidden=False)
    @checks.mod_or_permissions()
    async def writeteam(self, ctx, args):
        """I will write the name of your clan to my database \n You will need a 'Bot Commander' role in order to use this"""
        server = ctx.message.server
        teams = load_teams()
        d = teams
        d[server.id] = {}
        d[server.id]["team"] = args
        with open('teams.json', 'w') as fp:
            json.dump(d, fp, indent=2)
        await asyncio.sleep(1)
        await self.bot.say("I have successfully written your team's name into my database")

def setup(bot):
    bot.add_cog(Scoring(bot))
