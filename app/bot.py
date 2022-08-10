import asyncio
import datetime
import logging
import os
import random
import traceback

import discord

from app import config
from app import typings

__version__ = "0.3"

log = logging.getLogger("discord")
logging.basicConfig(level=config.LOGLEVEL)

class ExtBot(typings.ExtBotType):

  def __init__(self) -> None:
    intents = discord.Intents.all()

    super().__init__(command_prefix=config.PREFIX, intents=intents)

  async def random_activity(self) -> None:
    while True:
      members = list(self.get_all_members())
      memberCount = len(members)
      randomMember = random.choice(members)
      randomGame: typings.Game = random.choice(config.GAMES)

      await self.change_presence(activity=discord.Activity(
        type=randomGame.activity,
        name=randomGame.something.format(memberCount = memberCount, randomMember=randomMember)
      ))
      await self.on_activity_changed()
      await asyncio.sleep(config.GAMES_DELAY)

  async def on_activity_changed(self) -> None:
    pass

  async def on_ready(self) -> None:

    self.startTime = datetime.datetime.utcnow()
    self.botVersion = __version__
    self.appInfo = await self.application_info()
    self.gamesLoop = asyncio.ensure_future(self.random_activity())

    for filename in os.listdir("./app/cogs"):
      if filename.endswith(".py"):
        self.load_extension(f"app.cogs.{filename[:-3]}")

    log.info(f"Bot-Prefix: {self.command_prefix}")
    log.info(f"Bot-Name: {self.user} ({self.user.id})")
    log.info(f"Bot-Owner: {self.appInfo.owner} ({self.appInfo.owner.id})")
    log.info(f"Bot-Version: {self.botVersion}")
    log.info(f"Bot-Started-At: {self.startTime:%m/%d/%Y %H:%M:%S}")
    log.info(f"Pycord-Version: {discord.__version__}")

  async def on_guild_join(self, guild: discord.Guild) -> None:
    embed = discord.Embed(title=":white_check_mark: The bot added to new guild", type="rich", color=0x2ecc71)

    # embed.set_thumbnail(url=guild.icon.url)
    embed.add_field(name="Name", value=guild.name, inline=True)
    embed.add_field(name="ID", value=str(guild.id), inline=True)
    # embed.add_field(name="Owner", value=f"{guild.owner} ({guild.owner.id})", inline=True)
    # embed.add_field(name="Region", value=guild.region, inline=True)
    embed.add_field(name="Members", value=str(guild.member_count), inline=True)
    embed.add_field(name="Created on", value=str(guild.created_at), inline=True)

    await self.appInfo.owner.send(embed=embed)

  async def on_guild_remove(self, guild: discord.Guild) -> None:
    embed = discord.Embed(title=":x: The bot was kicked out of the guild", type="rich", color=0xe74c3c)

    # embed.set_thumbnail(url=guild.icon.url)
    embed.add_field(name="Name", value=guild.name, inline=True)
    embed.add_field(name="ID", value=str(guild.id), inline=True)
    # embed.add_field(name="Owner", value=f"{guild.owner} ({guild.owner.id})", inline=True)
    # embed.add_field(name="Region", value=guild.region, inline=True)
    embed.add_field(name="Members", value=str(guild.member_count), inline=True)
    embed.add_field(name="Created on", value=str(guild.created_at), inline=True)

    await self.appInfo.owner.send(embed=embed)

  async def on_error(self, event: str, *args, **kwargs) -> None:
    embed = discord.Embed(title=":exclamation: Event Error", colour=0xe74c3c)

    embed.add_field(name="Event", value=event)
    embed.description = f"```py\n{traceback.format_exc()}\n```"
    embed.timestamp = datetime.datetime.utcnow()

    await self.appInfo.owner.send(embed=embed)

  def run(self) -> None:
    super().run(config.TOKEN)
