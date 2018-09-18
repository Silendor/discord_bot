#!/usr/bin/env python3
import discord
import os

secret='DISCORD_BOT_SECRET'

def initialize_token():
    with open('.env', 'r') as filetype:
        os.environ[secret] = filetype.read().strip()

client = discord.Client()

@client.event
async def on_ready():
    await client.change_presence(game=discord.Game(name="с людишками"))
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
    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

initialize_token()
token = os.environ.get(secret)
client.run(token)