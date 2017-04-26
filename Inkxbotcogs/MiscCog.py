from discord.ext import commands
import asyncio
import discord

class Misc:
    """ Miscellaneous commands. """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, hidden=True)
    async def coreyrage(self, ctx):
        """Corey's rage"""
        await self.bot.send_typing(typetochan)
        await asyncio.sleep(1)
        await self.bot.say("I HATE EVERYTHING ARE YOU KIDDING ME RAAAAAAAAAAAAAAAAAAAGHHHHHHHHHHHHHHHHHHHHHHHFEIFYEDBJ")

    @commands.command(pass_context=True, name="break")
    async def _break(self, ctx):
        """Take a break"""
        typetochan = ctx.message.channel
        await self.bot.send_typing(typetochan)
        await asyncio.sleep(1)
        await self.bot.say("It's time to take a break. Or you'll probably never stop.")


    @commands.command(pass_context=True, hidden=True)
    async def ctkcryo(self, ctx):
        """cryo"""
        typetochan = ctx.message.channel
        await self.bot.send_typing(typetochan)
        await asyncio.sleep(1)
        await self.bot.say("PEW PEW PEW! PEW PEW PEW PEW PEW! SHUT THE FUCK UP")

    @commands.command(pass_context=True, hidden=True)
    async def coreygasm(self, ctx):
        """coreygasm"""
        typetochan = ctx.message.channel
        await self.bot.send_typing(typetochan)
        await asyncio.sleep(1)
        await self.bot.say("OMGOMGOMGOMGOMGFDEJWDVEJFVEJKVJEJR")

    @commands.command(pass_context=True, hidden=True)
    async def ctkmoment(self, ctx):
        """ctkmoment"""
        typetochan = ctx.message.channel
        await self.bot.send_typing(typetochan)
        await asyncio.sleep(1)
        await self.bot.say("OH THAT CTK *laugh track*")

    @commands.command(pass_context=True, hidden=True)
    async def zhuli(self, ctx):
        typetochan = ctx.message.channel
        await self.bot.send_typing(typetochan)
        await asyncio.sleep(1)
        await self.bot.say("Zhu Li, do the thing!")

    @commands.command(pass_context=True, hidden=True)
    async def beck(self, ctx):
        typetochan = ctx.message.channel
        await self.bot.send_typing(typetochan)
        await asyncio.sleep(1)
        await self.bot.say("That's more like it!")

    @commands.command(pass_context=True)
    async def slap(self, ctx, args):
        """Slap someone!"""
        typetochan = ctx.message.channel
        user = ctx.message.author.mention
        if args == "<@245648163837444097>":
            await self.bot.send_typing(typetochan)
            await asyncio.sleep(1)
            await self.bot.say("Don't think about slapping me \U0001f621")
        elif args == " <@245648163837444097> ":
            await self.bot.send_typing(typetochan)
            await asyncio.sleep(1)
            await self.bot.say("Don't think about slapping me \U0001f621")
        elif args == ctx.message.author.mention:
            await self.bot.send_typing(typetochan)
            await asyncio.sleep(1)
            await self.bot.say("Way to go, you just slaped yourself.")
        elif args == ctx.message.author.name:
            await self.bot.send_typing(typetochan)
            await asyncio.sleep(1)
            await self.bot.say("Way to go, you just slaped yourself.")
        elif args == "@everyone":
            await self.bot.send_typing(typetochan)
            await asyncio.sleep(1)
            await self.bot.say("That is totaly breaking the rules...")
        elif args == "@here":
            await self.bot.send_typing(typetochan)
            await asyncio.sleep(1)
            await self.bot.say("That is totaly breaking the rules...")
        elif args == "/@everyone":
            await self.bot.send_typing(typetochan)
            await asyncio.sleep(1)
            await self.bot.say("That is totaly breaking the rules...")
        elif args == "/@here":
            await self.bot.send_typing(typetochan)
            await asyncio.sleep(1)
            await self.bot.say("That is totaly breaking the rules...")
        elif args == "\@everyone":
            await self.bot.send_typing(typetochan)
            await asyncio.sleep(1)
            await self.bot.say("That is totaly breaking the rules...")
        elif args == "\@here":
            await self.bot.send_typing(typetochan)
            await asyncio.sleep(1)
            await self.bot.say("That is totaly breaking the rules...")
        else:
            await self.bot.send_typing(typetochan)
            await asyncio.sleep(1)
            await self.bot.say('**SMACK!** *{0} slaps {1}*'.format(user, args))

    @commands.command(pass_context=True)
    async def add(self, ctx):
        """I will give you a link so I can be added to a server"""
        typetochan = ctx.message.channel
        await self.bot.send_typing(typetochan)
        await asyncio.sleep(1)
        await self.bot.say('You want to add me to a server? Ok! Add me to a server with this link: https://discordapp.com/oauth2/authorize?client_id=245648163837444097&scope=bot&permissions=268437512')

    @commands.command(pass_context=True, hidden=True)
    async def typing(self, ctx):
        """A little test command to test to see if I'm typing"""
        typetochan = ctx.message.channel
        await self.bot.send_typing(typetochan)
        await asyncio.sleep(8)
        await self.bot.say("There, I'm done typing for you")



def setup(bot):
    bot.add_cog(Misc(bot))
