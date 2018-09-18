#!/usr/bin/env python3
import os
import logging
import json
import aiohttp
import asyncio
import discord
from discord import Game
# from discord.ext import commands
from discord.ext.commands import Bot

secret='DISCORD_BOT_SECRET'
description = '''Simple bot'''

'''
set up logging level:
CRITICAL
ERROR
WARNING
INFO
DEBUG
'''
# log output to console:
# logging.basicConfig(level=logging.ERROR)
# log to file:
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

def initialize_token():
    with open('.env', 'r') as filetype:
        os.environ[secret] = filetype.read().strip()

# client = discord.Client()
client = Bot(command_prefix='$', description=description)

@client.event
async def on_ready():
    # await client.change_presence(game=Game(name="с людишками"))
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    # if message.author != client.user:
    #     await client.send_message(message.channel, message.content[::-1])

    if message.content.startswith('?help'):
        await client.send_message(message.channel, msg)
################################################################
# experimental
################################################################
url = 'https://pubg.op.gg/user/Silendor?server=pc-ru'

@client.command()
async def bitcoin():
    url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
    async with aiohttp.ClientSession() as session:  # Async HTTP request
        raw_response = await session.get(url)
        response = await raw_response.text()
        response = json.loads(response)
        await client.say("Bitcoin price is: $" + response['bpi']['USD']['rate'])

################################################################
# /experimental
################################################################
initialize_token()
token = os.environ.get(secret)
client.run(token)