import sys

if __name__ != "__main__":
	sys.exit(1)

from app.bot import ExtBot

bot = ExtBot()
bot.run()