from discord.ext import commands
from .utils import config, checks
import asyncio
import discord

def load_messages():
    with open('servermessage.json') as m:
        return json.load(m)

class Moderation:
    """ Moderative Commands to keep the server clean """

    def __init__(self, bot):
        self.bot = bot



    def _role_from_string(self, server, rolename, roles=None):
        if roles is None:
            roles = server.roles
        role = discord.utils.find(lambda r: r.name.lower() == rolename.lower(),roles)

        return role


    @commands.command(pass_context=True, no_pm=True, name = 'clear')
    @commands.has_role('Bot Commander')
    async def _clear(self, ctx, amount : int = 100):
        """Deletes my messages. \n You will need a 'Bot Commander' role in order to use this"""
		
        channel = ctx.message.channel

        calls = 0;
        async for msg in self.bot.logs_from(channel, limit=amount, before=ctx.message):
            if calls and calls % 5 == 0:
                await asyncio.sleep(1.5)

            if msg.author == self.bot.user:
                await self.bot.delete_message(msg)
                calls += 1
        await self.bot.say('Deleted {0}'.format(calls))
        await asyncio.sleep(1.5)
        await self.bot.delete_message(channel, limit=1, after=ctx.message)

    @commands.command(pass_context=True, no_pm=True)
    @checks.mod_or_permissions()
    async def purge(self, ctx, amount : int = 5):
        """Deletes specified number of messages.
        You must have a 'Bot Commander' role in order to use this"""
        await self.bot.purge_from(ctx.message.channel, limit=amount, before=ctx.message)
        await self.bot.say('Deleted {0}'.format(amount))
        await asyncio.sleep(1.5)
        #await self.bot.delete_message(ctx.message.channel, limit=(1), after=ctx.message)

#    the command below is still in development. I'm sorry if the development is gonna take long

    @commands.command(pass_context=True, no_pm=True)
    @commands.has_role('Bot Commander')
    async def give(self, ctx, rolename, user: discord.Member=None):
        """Gives a role to a user, defaults to author
        Role name must be in quotes if there are spaces.
        You must have a 'Bot Commander' role in order to use this"""
        author = ctx.message.author
        channel = ctx.message.channel
        server = ctx.message.server

        if user is None:
            user = author

        role = self._role_from_string(server, rolename)

        if role is None:
            await self.bot.say('That role cannot be found.')
            return

        if not channel.permissions_for(server.me).manage_roles:
            await self.bot.say("I don't have permissions to manage roles!")
            return

        await self.bot.add_roles(user, role)
        await self.bot.say('I have given the {} role to {}'.format(role.name, user.name))

    @commands.command(pass_context=True, no_pm=True, name = 'remove')
    @checks.mod_or_permissions()
    async def _remove(self, ctx, rolename, user: discord.Member=None):
        """Removes a role from user, defaults to author
        Role name must be in quotes if there are spaces.
        You will need a 'Bot Commander' role in order to use this"""
        server = ctx.message.server
        author = ctx.message.author

        role = self._role_from_string(server, rolename)
        if role is None:
            await self.bot.say("Role not found.")
            return

        if user is None:
            user = author

        if role in user.roles:
            try:
                await self.bot.remove_roles(user, role)
                await self.bot.say("Role successfully removed.")
            except discord.Forbidden:
                await self.bot.say("I don't have permissions to manage roles!")
        else:
            await self.bot.say("User does not have that role.")

    #@commands.group(pass_context=True, no_pm=True)
    #@checks.mod_or_permissions()
    #async def welcome(self, ctx)
        #"""Shows your server's current welcome message or changes it. Bot Commander required"""
        #server = ctx.message.server
        #lm = load_messages()
        #wlc = lm[server.id]['welcome'].format('user')
        #await self.bot.say("**your server's current welcome message:** `{}`".format(wlc))

    #@welcome.command(pass_context=True, no_pm=True)
    #@checks.mod_or_permissions()
    #async def onjoin(self, ctx, args)
        #"""Sets the server's welcome message to when a new user joins the server"""
        #server= ctx.message.server
        #lm = load_messages()

def setup(bot):
    bot.add_cog(Moderation(bot))
