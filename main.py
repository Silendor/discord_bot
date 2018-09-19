#!/usr/bin/env python3
import os
import json
import aiohttp
# import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv

# custom libraries
from bot_logging import Bot_Logging

# 
logger_target = 'discord'
log_level = 'DEBUG'
discord_log = Bot_Logging(logger_target, log_level)
discord_log.log_to_file()

# client = discord.Client()
description = '''Simple bot'''
bot = commands.Bot(command_prefix='!', description=description)

@bot.event
async def on_ready():
    # await bot.change_presence(game=discord.Game(name="с людишками"))
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def hello(member : discord.Member):
    """Поднимает самооценку"""
    answer = 'Ты классный, {0.name} :thumbsup:'.format(member)
    await bot.say(answer)

@bot.command()
async def add(left : int, right : int):
    """Adds two numbers together."""
    await bot.say(left + right)

@bot.command()
async def btc():
    """Выводит текущий курс биткоина к доллару"""
    url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
    async with aiohttp.ClientSession() as session:  # Async HTTP request
        raw_response = await session.get(url)
        response = await raw_response.text()
        response = json.loads(response)
        await bot.say("Bitcoin price is: $" + response['bpi']['USD']['rate'])

# on_message() ловит все сообщения и блокирует .command()
# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return
#     if message.content.startswith('!hello'):
#         answer = 'Ты классный, {0.author.mention} :thumbsup:'.format(message)
#         await client.send_message(message.channel, answer)

################################################################
# ^experimental
################################################################

# @bot.command()
# async def opgg():
#     """Отдаёт статистику pubg по никнейму"""
#     api_key = os.environ.get('PUBG_API_SECRET')
#     url = "https://api.pubg.com/shards/$platform-region-shard/players?filter[playerNames]=$player-name"

#     header = {
#         "Authorization": "Bearer <api-key>",
#         "Accept": "application/vnd.api+json"
#         }

#     r = requests.get(url, headers=header)


################################################################
# $experimental
################################################################
# initialize environment settings
load_dotenv()

token = os.environ.get('DISCORD_BOT_SECRET')
bot.run(token)