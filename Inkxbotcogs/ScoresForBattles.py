from discord.ext import commands
import discord
import asyncio
import json


def write_teams():
    with open('teams.json') as fp:
        return json.dump()

def load_teams():
    with open('teams.json') as lt:
        return json.load(lt)


class Scoring:
    """Commands that display scores from e-sport battles against teams."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['p'], pass_context=True, no_pm=True, hidden=False)
    async def post(self, ctx, battle, homescr, args, awayscr):
        """posts a scrim score in a #scrim-scores channel \n EXAMPLE: ,post 'Tournament or Scrim' 2 'name of clan you scrimed against' 1"""
        teams = load_teams()
        if battle == 'scrim':
            battle = 'Scrim'
        else:
            battle = battle
        server = ctx.message.server
        teamserver = teams[server.id]
        teamname = teams[server.id]['team']
#                In the future, the command will also do tournament scores, but that will have to wait.
        for s in server.channels:
            if battle == 'Scrim':
                if s.name == "scrim-scores":
                    await self.bot.send_message(s, "**{4}** \n{0} {1}  -  {3} {2}".format(teamname, homescr, args, awayscr, battle))
                    await self.bot.say("done")
                    break
            elif server.id not in teams:
                await self.bot.say("You haven't given me your team's name, type `,writeteam \"YOUR TEAM'S NAME HERE\"` to store it into my database")
                break
        else:
            self.bot.say("It seems there's a problem, I don't see a #scrim-scores or a #tournament-scores")

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
        await self.bot.say("the content will be added to my database in a while")

def setup(bot):
    bot.add_cog(Scoring(bot))
