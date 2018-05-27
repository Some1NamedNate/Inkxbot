# -*- coding: utf-8 -*-

from discord.ext import commands
import discord

class Overwatch:
    """The description for OverwatchCog goes here."""

    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(Overwatch(bot))
