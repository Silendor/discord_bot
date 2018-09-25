#!/usr/bin/env python3
import os
import json
# import requests
import random
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

description = '''Simple newsletter bot'''
bot = commands.Bot(command_prefix='!', description=description)

@bot.event
async def on_ready():
    # await bot.change_presence(game=discord.Game(name="с людишками"))
    await bot.change_presence(game=discord.Game(name="в разработку"))
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command(pass_context=True)
async def hello(context):
    """Поднимает настроение"""
    possible_responses = [
        'Ты классный, {} :thumbsup:'.format(context.message.author.mention),
        'Весь мир вертится вокруг тебя, {} :earth_asia:'.format(context.message.author.mention),
        'За тобой выехали, {} :spy:'.format(context.message.author.mention),
        'Сегодня повезёт, {} :four_leaf_clover:'.format(context.message.author.mention),
        'Сегодня забухаем в :poop:, {}'.format(context.message.author.mention),
        'Мне нечего тебе сказать, {} :robot:'.format(context.message.author.mention),
    ]
    await bot.say(random.choice(possible_responses))

@bot.command()
async def btc():
    """Выводит текущий курс биткоина к доллару"""
    url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
    async with aiohttp.ClientSession() as session:  # Async HTTP request
        raw_response = await session.get(url)
        response = await raw_response.text()
        response = json.loads(response)
        await bot.say("Bitcoin price is: $" + response['bpi']['USD']['rate'])
####
# PUBG
####
@bot.command()
async def squadfpp(player_name=' '):
    """pubg Cтатистика squad-fpp игр по никнейму (RU)"""
    api_key = os.environ.get('PUBG_API_SECRET')
    shard = 'pc-ru'
    # shard = 'pc-eu'
    interest_mode = ('squad-fpp',)
    interest_items = ('winPoints', 'wins', 'top10s', 'assists', 
                'longestKill', 'maxKillStreaks', 'roundMostKills', 
                'suicides', 'vehicleDestroys')

    await bf.pubg_info(api_key, bot, shard, player_name, interest_mode, interest_items)

@bot.command()
async def squad(player_name=' '):
    """pubg Cтатистика squad-tpp игр по никнейму (RU)"""
    api_key = os.environ.get('PUBG_API_SECRET')
    shard = 'pc-ru'
    # shard = 'pc-eu'
    interest_mode = ('squad',)
    interest_items = ('winPoints', 'wins', 'top10s', 'assists', 
                'longestKill', 'maxKillStreaks', 'roundMostKills', 
                'suicides', 'vehicleDestroys')

    await bf.pubg_info(api_key, bot, shard, player_name, interest_mode, interest_items)

@bot.command()
async def duofpp(player_name=' '):
    """pubg Cтатистика duo-fpp игр по никнейму (RU)"""
    api_key = os.environ.get('PUBG_API_SECRET')
    shard = 'pc-ru'
    # shard = 'pc-eu'
    interest_mode = ('duo-fpp',)
    interest_items = ('winPoints', 'wins', 'top10s', 'assists', 
                'longestKill', 'maxKillStreaks', 'roundMostKills', 
                'suicides', 'vehicleDestroys')

    await bf.pubg_info(api_key, bot, shard, player_name, interest_mode, interest_items)

@bot.command()
async def duo(player_name=' '):
    """pubg Cтатистика duo-tpp игр по никнейму (RU)"""
    api_key = os.environ.get('PUBG_API_SECRET')
    shard = 'pc-ru'
    # shard = 'pc-eu'
    interest_mode = ('duo',)
    interest_items = ('winPoints', 'wins', 'top10s', 'assists', 
                'longestKill', 'maxKillStreaks', 'roundMostKills', 
                'suicides', 'vehicleDestroys')

    await bf.pubg_info(api_key, bot, shard, player_name, interest_mode, interest_items)

@bot.command()
async def solofpp(player_name=' '):
    """pubg Cтатистика solo-fpp игр по никнейму (RU)"""
    api_key = os.environ.get('PUBG_API_SECRET')
    shard = 'pc-ru'
    # shard = 'pc-eu'
    interest_mode = ('solo-fpp',)
    interest_items = ('winPoints', 'wins', 'top10s', 'assists', 
                'longestKill', 'maxKillStreaks', 'roundMostKills', 
                'suicides', 'vehicleDestroys')

    await bf.pubg_info(api_key, bot, shard, player_name, interest_mode, interest_items)

@bot.command()
async def solo(player_name=' '):
    """pubg Cтатистика solo-tpp игр по никнейму (RU)"""
    api_key = os.environ.get('PUBG_API_SECRET')
    shard = 'pc-ru'
    # shard = 'pc-eu'
    interest_mode = ('solo-fpp',)
    interest_items = ('winPoints', 'wins', 'top10s', 'assists', 
                'longestKill', 'maxKillStreaks', 'roundMostKills', 
                'suicides', 'vehicleDestroys')

    await bf.pubg_info(api_key, bot, shard, player_name, interest_mode, interest_items)

################################################################
# ^experimental
################################################################


################################################################
# $experimental
################################################################

# initialize environment settings
load_dotenv()
token = os.environ.get('DISCORD_BOT_SECRET')
# start bot
bot.run(token)