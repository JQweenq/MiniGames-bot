import os
import discord
from app import typings

LOGLEVEL: str = os.getenv("LOGLEVEL", "INFO")
PREFIX: str = os.getenv("PREFIX", ">")
TOKEN: str | None = os.getenv("TOKEN", None)

GAMES: list[typings.Game] = [
  typings.Game(discord.ActivityType.playing, "with Josty"),
  typings.Game(discord.ActivityType.watching, "Hentai"),
  typings.Game(discord.ActivityType.listening, "{randomMember}")
]

GAMES_DELAY: int = 60 * 5