from discord.ext import commands
from .utils import challongeaddon
import asyncio, aiohttp
from urllib.parse import quote as urlquote
import random
from collections import namedtuple
import discord

class Tournaments:
	""" Commands that gather information from challonge.com """
