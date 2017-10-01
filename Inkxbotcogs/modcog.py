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


    @commands.command(name = 'clear', invoke_without_command=True)
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def _clear(self, ctx, amount : int = 100):
        """Deletes my messages.
        You must have permissions to manage messages in order to use this"""

        channel = ctx.message.channel
        calls = 0;
        async for msg in channel.history(limit=amount, before=ctx.message):
            if calls and calls % 5 == 0:
                await asyncio.sleep(1.5)

            if msg.author == self.bot.user:
                await msg.delete()
                calls += 1
        await ctx.send('Deleted {0}'.format(calls), delete_after=3.0)

    @commands.command(name = 'clean', invoke_without_command=True, hidden=True)
    @commands.guild_only()
    @commands.is_owner()
    async def clean(self, ctx, amount : int = 100):
        channel = ctx.message.channel
        calls = 0;
        async for msg in channel.history(limit=amount, before=ctx.message):
            if calls and calls % 5 == 0:
                await asyncio.sleep(1.5)

            if msg.author == self.bot.user:
                await msg.delete()
                calls += 1
        await ctx.send('Deleted {0}'.format(calls), delete_after=3.0)


    @commands.command(invoke_without_command=True)
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount : int = 5):
        """Deletes specified number of messages.
        You must have permissions to manage messages in order to use this"""
        channel = ctx.message.channel
        message = ctx.message
        deleted = await channel.purge(limit=amount, before=message)
        await ctx.send('Deleted {}'.format(len(deleted)), delete_after=3.0)

    @commands.command(pass_context=True)
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def give(self, ctx, rolename, user: discord.Member=None):
        """Gives a role to a user, defaults to author
        Role name must be in quotes if there are spaces.
        You must have permissions to manage roles in order to use this"""
        if user is None:
            user = ctx.message.author

        role = self._role_from_string(server, rolename)

        if role is None:
            await ctx.trigger_typing()
            await asyncio.sleep(1)
            await ctx.send('That role cannot be found.')
            return

        if not channel.permissions_for(server.me).manage_roles:
            await ctx.trigger_typing()
            await asyncio.sleep(1)
            await ctx.send("I don't have permissions to manage roles!")
            return

        await ctx.trigger_typing()
        await self.bot.add_roles(user, role)
        await asyncio.sleep(1)
        await ctx.send('I have given the {} role to {}'.format(role.name, user.name))

    @commands.command(pass_context=True, name = 'remove')
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def _remove(self, ctx, rolename, user: discord.Member=None):
        """Removes a role from user, defaults to author
        Role name must be in quotes if there are spaces.
        You must have permissions to manage roles in order to use this"""
        role = self._role_from_string(server, rolename)
        if role is None:
            await ctx.trigger_typing()
            await asyncio.sleep(1)
            await ctx.send("Role not found.")
            return

        if user is None:
            user = author

        if role in user.roles:
            try:
                await ctx.trigger_typing()
                await self.bot.remove_roles(user, role)
                await asyncio.sleep(1)
                await ctx.send("Role successfully removed.")
            except discord.Forbidden:
                await ctx.trigger_typing()
                await asyncio.sleep(1)
                await ctx.send("I don't have permissions to manage roles!")
        else:
            await ctx.trigger_typing()
            await asyncio.sleep(1)
            await ctx.send("User does not have that role.")

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
