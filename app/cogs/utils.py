import datetime
import platform

import discord
from app import typings
from discord.ext import commands


class Utils(commands.Cog):

  def __init__(self, bot: typings.ExtBotType) -> None:
    self.bot = bot

  @commands.command(name="status")
  async def status(self, ctx: discord.ApplicationContext) -> None:
    uptimeDelta: datetime.timedelta = datetime.datetime.utcnow() - self.bot.startTime

    days = uptimeDelta.days
    hours, rem = divmod(uptimeDelta.seconds, 3600)
    minutes, seconds = divmod(rem, 60)

    users = 0
    channels = 0

    for guild in self.bot.guilds:
      users += len(guild.members)
      channels += len(guild.channels)

    embed = discord.Embed(title=":information_source: Information about this bot:", color=ctx.me.top_role.colour)

    embed.description = "You can find the source code [there](https://github.com/ilfey/Simple-bot)"

    embed.set_thumbnail(url=ctx.me.avatar.url)

    embed.add_field(name="Owner", value=str(self.bot.appInfo.owner), inline=False)
    embed.add_field(name="Start", value=self.bot.startTime.strftime("%m/%d/%Y %H:%M:%S"), inline=True)
    embed.add_field(name="Uptime", value=f"{days} days {hours}:{minutes}:{seconds}", inline=True)
    embed.add_field(name="Users", value=str(users), inline=True)
    embed.add_field(name="Servers", value=str(len(self.bot.guilds)), inline=True)
    embed.add_field(name="Channels", value=str(channels), inline=True)
    embed.add_field(name="Bot", value=self.bot.botVersion, inline=True)
    embed.add_field(name="Py-cord", value=discord.__version__, inline=True)
    embed.add_field(name="Python", value=platform.python_version(), inline=True)
    embed.add_field(name="OS", value=f"{platform.system()} {platform.release()} {platform.version()}", inline=False)

    await ctx.send(embed=embed)

  @commands.command(name="ping")
  async def ping(self, ctx: discord.ApplicationContext) -> None:
    embed = discord.Embed(title=":ping_pong: Pong!", color=0x7bf42a)

    pong = await ctx.send(embed=embed)

    delta = pong.created_at - ctx.message.created_at
    delta = int(delta.total_seconds() * 1000)

    embed.add_field(name="Latency", value=f"{delta} ms")
    embed.add_field(name="WS latency", value=f"{round(self.bot.latency, 5)} ms")

    await pong.edit(embed=embed)


def setup(bot: typings.ExtBotType) -> None:
  bot.add_cog(Utils(bot))
