#!/usr/bin/env python3
import os
import json
import requests
import aiohttp
# import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv

# custom libraries
from bot_logging import Bot_Logging
import functions as bf 

# log settings
logger_target = 'discord'
log_level = 'DEBUG'
discord_log = Bot_Logging(logger_target, log_level)
discord_log.log_to_file()

description = '''Simple bot'''
bot = commands.Bot(command_prefix='!', description=description)

@bot.event
async def on_ready():
    # await bot.change_presence(game=discord.Game(name="с людишками"))
    await bot.change_presence(game=discord.Game(name="в разработку"))
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

@bot.command()
async def repeat(times : int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await bot.say(content)

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

@bot.command()
async def opgg(player_name=' '):
    """Отдаёт статистику pubg по никнейму"""

    interest_mode = ('squad-fpp',)
    interest_items = ('winPoints', 'wins', 'top10s', 'assists', 
                'longestKill', 'maxKillStreaks', 'roundMostKills', 
                'suicides', 'vehicleDestroys')

    if player_name is ' ':
        await bot.say('Укажи никнейм')
    else:
        api_key = os.environ.get('PUBG_API_SECRET')
        shard = 'pc-ru'       
        player_id = bf.get_player_info(shard, player_name, api_key)
        if player_id == 'Not Found':
            await bot.say('Такой ник не найден в базе')
        else:
            season_id = bf.get_season_info(shard, api_key)
            if season_id == 'Not Found':
                await bot.say('Актуальный сезон не обнаружен')
            else:
                general_info = bf.get_general_stat_info(shard, player_id, season_id, api_key, interest_mode, interest_items)
                if general_info == 'Not Found':
                    await bot.say('Никнейм найден, актуальный сезон найден, статистика почему-то недоступна :cry:')
                else:
                    for mode in general_info:
                        await bot.say(mode.capitalize() + ':')
                        for key, value in general_info[mode][0].items():
                            await bot.say(key + ' - ' + str(value))

################################################################
# $experimental
################################################################
# initialize environment settings
load_dotenv()

token = os.environ.get('DISCORD_BOT_SECRET')
bot.run(token)