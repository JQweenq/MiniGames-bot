from discord.ext import commands
import traceback
import datetime
import discord
import logging
import asyncio
import config
import random
import time
import os


__version__ = "0.1"

log = logging.getLogger("discord")
logging.basicConfig(level=config.logLevel)


class ExtClient(commands.AutoShardedBot):

	def __init__(self):
		intents = discord.Intents.default()

		super().__init__(command_prefix=config.prefix, intents=intents)

	async def random_activity(self):
		while True:
			members = list(self.get_all_members())
			memberCount = len(members)
			randomMember = random.choice(members)
			randomGame = random.choice(config.games)
			await self.change_presence(activity=discord.Activity(type=randomGame[0], name=randomGame[1].format(memberCount = memberCount, randomMember=randomMember)))
			await self.on_activity_changed()
			await asyncio.sleep(config.gamesDelay)

	async def on_activity_changed(self):
		pass

	async def on_ready(self):
		self.startTime = time.time()
		self.botVersion = __version__
		self.appInfo = await self.application_info()

		log.info(f"Bot-Name: {self.user}")
		log.info(f"Bot-ID: {self.user.id}")
		log.info(f"Bot-Owner: {self.appInfo.owner}")
		log.info(f"Bot-Version: {self.botVersion}")
		log.info(f"Bot-Start-Time: {self.startTime}")
		log.info(f"Pycord-Version: {discord.__version__}")

		await self.random_activity()

	async def on_message(self, message: discord.Message):
		pass

	async def on_member_join(self, member):
		pass

	async def on_member_remove(self, member):
		pass

	async def on_guild_join(self, guild: discord.Guild):
		embed = discord.Embed(title=":white_check_mark: The bot added to new guild", type="rich", color=0x2ecc71)

		embed.set_thumbnail(url=guild.icon.url)
		embed.add_field(name="Name", value=guild.name, inline=True)
		embed.add_field(name="ID", value=guild.id, inline=True)
		embed.add_field(name="Owner", value=f"{guild.owner} ({guild.owner.id})", inline=True)
		embed.add_field(name="Region", value=guild.region, inline=True)
		embed.add_field(name="Members", value=guild.member_count, inline=True)
		embed.add_field(name="Created on", value=guild.created_at, inline=True)

		await self.appInfo.owner.send(embed=embed)

	async def on_guild_remove(self, guild: discord.Guild):
		embed = discord.Embed(title=":x: The bot was kicked out of the guild", type="rich", color=0xe74c3c)

		embed.set_thumbnail(url=guild.icon.url)
		embed.add_field(name="Name", value=guild.name, inline=True)
		embed.add_field(name="ID", value=guild.id, inline=True)
		embed.add_field(name="Owner", value=f"{guild.owner} ({guild.owner.id})", inline=True)
		embed.add_field(name="Region", value=guild.region, inline=True)
		embed.add_field(name="Members", value=guild.member_count, inline=True)
		embed.add_field(name="Created on", value=guild.created_at, inline=True)

		await self.appInfo.owner.send(embed=embed)

	async def on_error(self, event: str, *args, **kwargs):
		embed = discord.Embed(title=":exclamation: Event Error", colour=0xe74c3c)

		embed.add_field(name="Event", value=event)
		embed.description = f"```py\n{traceback.format_exc()}\n```"
		embed.timestamp = datetime.datetime.utcnow()

		await self.appInfo.owner.send(embed=embed)


	async def on_command_error(self):
		pass


if __name__	== "__main__":
	client = ExtClient()
	client.run(config.token)