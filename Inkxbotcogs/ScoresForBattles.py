# This Code is where I try to match the discord.py rewrite, it's not ready yet.
# 

from discord.ext import commands
import discord
import asyncio
import json


def write_teams():
    with open('teams.json') as f:
        return json.dump()

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
    async def post(self, ctx, battle, homescr, args, awayscr):
        """posts a scrim score in a #scrim-scores channel \n EXAMPLE: ,post 'Tournament or Scrim' 2 'name of clan you scrimed against' 1"""
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
                    await ctx.send("done")
                    break
            elif battle == battle:
                if s.name == "tournament-scores":
                    await self.bot.send_message(s, "**Tournament**: {4} \n{0} {1}  -  {3} {2}".format(teamname, homescr, args, awayscr, trnyname))
                    await ctx.send("done")
                    break

            elif server.id not in teams:
                await ctx.send("You haven't given me your team's name, type `,writeteam \"YOUR TEAM'S NAME HERE\"` to store it into my database")
                break

            elif battle not in trnys:
                if s.name == "tournament-scores":
                    await self.bot.send_message(s, "**Tournament**: {4} \n{0} {1}  -  {3} {2}".format(teamname, homescr, args, awayscr, battle))
                    await ctx.send("The tourament's name is not in my database yet but I'll still post it.")
                    break

        else:
            await self.bot.say("It seems there's a problem, try again")

    @commands.command(aliases=['wt'], pass_context=True, no_pm=True, hidden=False)
    async def writeteam(self, ctx, args):
        """I will write the name of your clan to my database"""
        server = ctx.message.server
        user = ctx.message.author
#                In the future, the command will write to the json by itself. But for now, I have to do it.
        #data = {'{}'.format(server.id):{'team': '{}'.format(args)}
        #        }
        #file = open('teams.json', 'w')
        #json.dump(obj=data, fp=file, indent=4)
        #await asyncio.sleep(1)
        #await self.bot.say("I have successfully written your team's name into my database")
        print('"{0}: {1}" Requested by {2}'.format(server.id, args, user))
        print('----------------------------------------------')
        await ctx.send("the content will be added to my database in a while")

def setup(bot):
    bot.add_cog(Scoring(bot))
