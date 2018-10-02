#!/usr/bin/env python3
import os
import json
import aiohttp
import discord
from discord.ext import commands
from dotenv import load_dotenv
# import requests
# import asyncio

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
bot_id = '490361317262229541'

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
    await bf.hello_random(bot, context)

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
async def link():
    '''Выдаёт ссылку на добавление бота на сервер'''
    url='https://discordapp.com/oauth2/authorize?client_id=490361317262229541&scope=bot'
    await bot.say(url)

####
# PUBG
####
@bot.command(pass_context=True)
async def squadfpp(context, player_name=' '):
    """pubg Cтатистика squad-fpp игр по никнейму (RU)"""
    api_key = os.environ.get('PUBG_API_SECRET')
    shard = 'pc-ru'
    # shard = 'pc-eu'
    interest_mode = ('squad-fpp',)
    interest_items = ('winPoints', 'wins', 'top10s', 'assists', 
                'longestKill', 'maxKillStreaks', 'roundMostKills', 
                'suicides', 'vehicleDestroys')

    await bf.pubg_info(api_key, bot, shard, player_name, interest_mode, interest_items, context)

@bot.command(pass_context=True)
async def squad(context, player_name=' '):
    """pubg Cтатистика squad-tpp игр по никнейму (RU)"""
    api_key = os.environ.get('PUBG_API_SECRET')
    shard = 'pc-ru'
    # shard = 'pc-eu'
    interest_mode = ('squad',)
    interest_items = ('winPoints', 'wins', 'top10s', 'assists', 
                'longestKill', 'maxKillStreaks', 'roundMostKills', 
                'suicides', 'vehicleDestroys')

    await bf.pubg_info(api_key, bot, shard, player_name, interest_mode, interest_items, context)

@bot.command(pass_context=True)
async def duofpp(context, player_name=' '):
    """pubg Cтатистика duo-fpp игр по никнейму (RU)"""
    api_key = os.environ.get('PUBG_API_SECRET')
    shard = 'pc-ru'
    # shard = 'pc-eu'
    interest_mode = ('duo-fpp',)
    interest_items = ('winPoints', 'wins', 'top10s', 'assists', 
                'longestKill', 'maxKillStreaks', 'roundMostKills', 
                'suicides', 'vehicleDestroys')

    await bf.pubg_info(api_key, bot, shard, player_name, interest_mode, interest_items, context)

@bot.command(pass_context=True)
async def duo(context, player_name=' '):
    """pubg Cтатистика duo-tpp игр по никнейму (RU)"""
    api_key = os.environ.get('PUBG_API_SECRET')
    shard = 'pc-ru'
    # shard = 'pc-eu'
    interest_mode = ('duo',)
    interest_items = ('winPoints', 'wins', 'top10s', 'assists', 
                'longestKill', 'maxKillStreaks', 'roundMostKills', 
                'suicides', 'vehicleDestroys')

    await bf.pubg_info(api_key, bot, shard, player_name, interest_mode, interest_items, context)

@bot.command(pass_context=True)
async def solofpp(context, player_name=' '):
    """pubg Cтатистика solo-fpp игр по никнейму (RU)"""
    api_key = os.environ.get('PUBG_API_SECRET')
    shard = 'pc-ru'
    # shard = 'pc-eu'
    interest_mode = ('solo-fpp',)
    interest_items = ('winPoints', 'wins', 'top10s', 'assists', 
                'longestKill', 'maxKillStreaks', 'roundMostKills', 
                'suicides', 'vehicleDestroys')

    await bf.pubg_info(api_key, bot, shard, player_name, interest_mode, interest_items, context)

@bot.command(pass_context=True)
async def solo(context, player_name=' '):
    """pubg Cтатистика solo-tpp игр по никнейму (RU)"""
    api_key = os.environ.get('PUBG_API_SECRET')
    shard = 'pc-ru'
    # shard = 'pc-eu'
    interest_mode = ('solo-fpp',)
    interest_items = ('winPoints', 'wins', 'top10s', 'assists', 
                'longestKill', 'maxKillStreaks', 'roundMostKills', 
                'suicides', 'vehicleDestroys')

    await bf.pubg_info(api_key, bot, shard, player_name, interest_mode, interest_items, context)

################################################################
# ^experimental
################################################################
@bot.command(pass_context=True)
async def test(context):
    '''тестовый пункт меню для нового функционала'''
    em = discord.Embed(title="Title", description="Desc", color=0x50bdfe)
    em.add_field(name="Field1", value="hi", inline=False)
    em.add_field(name="Field2", value="hi2", inline=False)
    await bot.say(embed=em)

################################################################
# $experimental
################################################################

# initialize environment settings
load_dotenv()
token = os.environ.get('DISCORD_BOT_SECRET')
# start bot
bot.run(token)