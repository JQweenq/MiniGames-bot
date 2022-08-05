import discord
import typings
import os

logLevel: str = os.getenv("LOGLEVEL", "INFO")
prefix: str = os.getenv("PREFIX", ">")
token: str = os.getenv("TOKEN", None)

games: list[typings.Game] = [
	typings.Game(discord.ActivityType.playing, "with Josty"),
	typings.Game(discord.ActivityType.watching, "Hentai"),
	typings.Game(discord.ActivityType.listening, "{randomMember}")
]

gamesDelay: int = 60 * 5