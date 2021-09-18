from discord.ext import commands
from time import time
import discord
import json
import random

js = json.load(open("config.json", "r+", encoding='utf-8'))


client = commands.Bot(command_prefix=js["prefix"], intents=discord.Intents.all())

# Изменение статуса бота
@client.event
async def on_connect():
	print(js['prefix'])
	await client.change_presence(status = discord.Status.idle, activity = discord.Game("DurkaHub"))

# Команда clear
@client.command(name="удали", help="Удаляет определенное кол-во сообщений.")
async def clear(ctx, amount = 100):
	await ctx.channel.purge(limit = amount)
	if amount == 1:
		await ctx.send("Я удалила " + str(amount) + " сообщение.")
	elif 1 < amount < 5:
		await ctx.send("Я удалила " + str(amount) + " сообщения.")
	elif 5 < amount:
		await ctx.send("Я удалила " + str(amount) + " сообщений.")


# Команда send
@client.command(name="отправь", help="Отправляет сообщение от имени бота.")
async def send(ctx, *, args):
	await ctx.send(args)


# Команда prefix
@client.command(name="префикс", help="Показывает доступные префиксы.")
async def prefix(ctx):
	await ctx.channel.send(f'`{js["prefix"]}`')


@client.command(name="число c", help="Генерирует рандомное число с количеством символов")
async def rint(ctx, amount):
	msg = ''
	for _ in range(int(amount)):
		msg += str(random.randint(0, 9))
	await ctx.channel.send(msg)


@client.command(name="число", help="Генерирует рандомное число")
async def rint(ctx, _from = 1, to = 100):
	
	await ctx.channel.send(str(random.randint(_from, to)))

@client.command(name="помощь", help="Вызывает команду help")
async def rint(ctx):
	await ctx.send_help()


@client.command(name="аватар", help="Отправляет аватарку из ID")
async def rint(ctx, user: discord.User):
	await ctx.channel.send(user.avatar_url)


@client.command(name="аватарка", help="Отправляет аватарку через пинг")
async def rint(ctx, user: discord.Member):
	await ctx.channel.send(user.avatar_url)


# Запуск бота
client.run(js["token"])
