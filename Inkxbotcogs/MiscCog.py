from discord.ext import commands
import asyncio
import discord


class Misc:
    """ Miscellaneous commands. """
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(hidden=True)
    async def coreyrage(self):
        """Corey's rage"""
        await self.bot.say("I HATE EVERYTHING ARE YOU KIDDING ME RAAAAAAAAAAAAAAAAAAAGHHHHHHHHHHHHHHHHHHHHHHHFEIFYEDBJ")
    
    @commands.command()
    async def _break(self):
        """Take a break"""
        await self.bot.say("It's time to take a break. Or you'll probably never stop.")
        
    
    @commands.command(hidden=True)
    async def ctkcryo(self):
        """cryo"""
        await self.bot.say("PEW PEW PEW! PEW PEW PEW PEW PEW! SHUT THE FUCK UP")
	
    @commands.command()
    async def cryo(self):
        """I will imitate Cryo"""
        await self.bot.say("PEW PEW PEW! PEW PEW PEW PEW PEW! SHUT THE F##K UP")
    
    @commands.command(hidden=True)
    async def coreygasm(self):
        """coreygasm"""
        await self.bot.say("OMGOMGOMGOMGOMGFDEJWDVEJFVEJKVJEJR")
    
    @commands.command(hidden=True)
    async def ctkmoment(self):
	    """ctkmoment"""
	    await self.bot.say("OH THAT CTK *laugh track*")
    
    @commands.command(hidden=True)
    async def zhuli(self):
	    await self.bot.say("Zhu Li, do the thing!")
    
    @commands.command(hidden=True)
    async def beck(self):
        await self.bot.say("That's more like it!")
    
def setup(bot):
    bot.add_cog(Misc(bot))
