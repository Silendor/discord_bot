#!/usr/bin/env python3
import discord
import os

def set_environment_variable_token():
    with open('.env', 'r') as filetype:
        os.environ['DISCORD_BOT_SECRET'] = filetype.read()

client = discord.Client()

@client.event
async def on_ready():
    print("I'm in")
    print(client.user)

@client.event
async def on_message(message):
    if message.author != client.user:
        await client.send_message(message.channel, message.content[::-1])

set_environment_variable_token()
token = os.environ.get("DISCORD_BOT_SECRET")
client.run(token)