from discord.ext import commands
from .utils import checks
import datetime
import random
import asyncio
import discord
import logging
import aiohttp
import yarl
import json
import re

log = logging.getLogger(__name__)


# There's going to be some code duplication here because it's more
# straightforward than trying to be clever, I guess.
# I hope at one day to fix this and make it not-so-ugly.
# Hopefully by completely dropping Splatoon 1 support in
# the future.


class Splatoon:
    """Splatoon related commands."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context = True)
    async def schedule(self, ctx):
        """Shows the current Splatoon 2 schedule."""
        ctx.send("`Currently working on it, it's still in the idea phase...` ~Inkx")

def setup(bot):
    bot.add_cog(Splatoon(bot))