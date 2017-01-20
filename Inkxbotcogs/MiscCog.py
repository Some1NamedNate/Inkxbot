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
    
    @commands.command(name="break")
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
        
    @commands.command(pass_context=True)
    async def slap(self, ctx, args):
        """Slap someone!"""
        user = ctx.message.author.mention
        await self.bot.say('**SMACK!** *{0} slaps {1}*'.format(user, args)) 
    
    @commands.command()
    async def join(self):
        """I will give you a link so I can be added to a server"""
        await self.bot.say('You want me to join a server? Ok! Add me to a server by using this link: https://discordapp.com/oauth2/authorize?client_id=245648163837444097&scope=bot&permissions=268437512')

    @commands.command()
    async def inkxbot(self):
        """All about me!"""
        await self.bot.say("Hi! I'm Inkxbot! I was created by InkxtheSquid to be used as a tool for many purposes! type ``,,help`` to see my list of commands! Check the blog at <https://inkxbot.wordpress.com/> (Note: all my commands are not implemented yet, so I'm not finished yet)")
    
    #the following command is still in development
    @commands.command()
    async def invite(ctx):
        """I'll post your server's invite link in the chat"""
        #server = ctx.message.server
        #if server.id == '':
        #    await bot.say("")
        #else: 
        #    await bot.say("Please contact my owner if you want me to use this")
 
    @commands.command(hidden=True)
    async def play(self):
        await self.bot.say("I don't have music functions, but I'll have them in the future")
        
def setup(bot):
    bot.add_cog(Misc(bot))
