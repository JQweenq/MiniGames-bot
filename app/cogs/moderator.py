import datetime

import discord

from app import typings
from discord.ext import commands


class Moderator(commands.Cog):

  def __init__(self, bot: typings.ExtBotType) -> None:
    self.bot = bot

  @commands.command(aliases=["cls"])
  @commands.has_permissions(manage_messages=True)
  async def clear(self, ctx: discord.ApplicationContext, amount: int = 100) -> None:
    await ctx.channel.purge(limit=amount)

    await ctx.send(f":put_litter_in_its_place: {amount} messages deleted!")

  async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
    if isinstance(error, commands.errors.BadArgument):
      embed = discord.Embed(title=":exclamation: Command Error", colour=0xe74c3c)

      embed.description = f"```py\nSorry, you need to enter a number value!\n```"
      embed.timestamp = datetime.datetime.utcnow()

      await ctx.send(embed=embed, reference=ctx.message)
    else:
      raise error


def setup(bot: typings.ExtBotType) -> None:
  bot.add_cog(Moderator(bot))
