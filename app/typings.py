import datetime
from collections import namedtuple

import discord
from discord.ext import commands

Game = namedtuple("Game", ["activity", "something"])


class ExtBotType(commands.AutoShardedBot):
	startTime: datetime.datetime
	appInfo: discord.AppInfo
	botVersion: str
	user: discord.ClientUser