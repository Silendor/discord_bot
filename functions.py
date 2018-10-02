import os
# import logging
import json
import random
import requests
import asyncio
import discord
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options

# caching
cache_opts = {
    'cache.type': 'file',
    'cache.data_dir': '/tmp/cache/data',
    'cache.lock_dir': '/tmp/cache/lock'
}
 
cache = CacheManager(**parse_cache_config_options(cache_opts))

# logging
# logging.basicConfig(filename="bot_error.log",filemode="w" , level=logging.ERROR)
# log = logging.getLogger("ex")

def api_call(api_key, url):
    header = {
            "Authorization": "Bearer {}".format(api_key),
            "Accept": "application/vnd.api+json",
            "Accept-Encoding":"gzip"
            }

    r = requests.get(url, headers=header)
    return r.json()
    # return requests.get(url, headers=header)

@cache.cache('get_player_func', type="file", expire=300)
def get_player_info(api_key, shard, player_name):
    '''get info about player'''
    url_player = "https://api.pubg.com/shards/{}/players?filter[playerNames]={}".format(shard, player_name)
    player_info = api_call(api_key, url_player)
    try:
        player_id = player_info['data'][0]['id']
    except KeyError:
        # player_id = player_info['errors'][0]['title']
        player_id = False
        # log.exception("Invalid answer structure get_player_info")
    return player_id

@cache.cache('get_season_func', type="file", expire=2592000)
def get_season_info(api_key, shard):
    '''get info about current season'''
    url_season = "https://api.pubg.com/shards/{}/seasons".format(shard)
    # season_id = 'division.bro.official.2018-09'
    season_info = api_call(api_key, url_season)
    season_num = len(season_info['data'])
    try:
        season_id = season_info['data'][season_num-1]['id']
    except KeyError:
        season_id = False
        # log.exception("Invalid answer structure get_season_info")
    return season_id

@cache.cache('get_general_stat_func', type="file", expire=300)
def get_general_stat_info(api_key, shard, player_id, season_id,
                            interest_mode, interest_items):
    '''get info about user statistics'''
    url_stat = 'https://api.pubg.com/shards/{}/players/{}/seasons/{}'.format(shard, player_id, season_id)
    general_info = api_call(api_key, url_stat)

    result = {}
    items_dict = {}
    for mode in interest_mode:
        for item in interest_items:
            try:
                value = general_info['data']['attributes']['gameModeStats'][mode].get(item)
            except KeyError:
                value = ''
                # log.exception("Invalid structure get_general_stat_info")
            # add smilies to categories
            item += add_smile(item)
            items_dict[item] = value
        result[mode] = [items_dict]
    return result

async def check_result(bot, player_name, general_info):
    '''handles errors and displays the result'''
    for mode in general_info:
        if all(value == 0 for value in general_info[mode][0].values()):
            answer = 'Статистики по этому режиму нет.'
            await bot.say(answer)
        elif all(value == '' for value in general_info[mode][0].values()):
            answer = 'Ошибка получения статистики.'
            await bot.say(answer)
        else:
            em_answer = discord.Embed(title=mode.capitalize(), description=player_name, color=0x50bdfe)
            for key, value in general_info[mode][0].items():
                em_answer.add_field(name=key, value=value, inline=False)
            await bot.say(embed=em_answer)

async def pubg_info(api_key, bot, shard, player_name, interest_mode, 
                    interest_items, context):
    '''collect complex information about player'''
    if player_name is ' ':
        answer = 'Укажи никнейм, {}'.format(context.message.author.mention)
        await bot.say(answer)
    else:
        player_id = get_player_info(api_key, shard, player_name)
        if player_id is False:
            answer = 'Такой ник не найден в базе, {}'.format(context.message.author.mention)
            await bot.say(answer)
        else:
            season_id = get_season_info(api_key, shard)
            if season_id is False:
                answer = 'Актуальный сезон не обнаружен'
                await bot.say(answer)
            else:
                # cache.invalidate(get_general_stat_info, 'get_general_stat_func')
                general_info = get_general_stat_info(api_key, shard, player_id, 
                                                    season_id, interest_mode, 
                                                    interest_items)
                await check_result(bot, player_name, general_info)

def add_smile(item):
    '''add discord smile to string where item from interest_items'''
    if item == 'winPoints':
        return ' :trophy:'
    elif item == 'wins':
        return ' :first_place:'
    elif item == 'top10s':
        return ' :second_place:'
        # return ' :top:'
    elif item == 'assists':
        return ' :handshake:'
    elif item == 'longestKill':
        return ''
    elif item == 'maxKillStreaks':
        return ''
    elif item == 'roundMostKills':
        return ''
    elif item == 'suicides':
        return ' :skull:'
    elif item == 'vehicleDestroys':
        return ' :red_car:'

async def hello_random(bot, context):
    '''selects a random response to the hello request'''
    possible_responses = [
        'Ты классный, {} :thumbsup:'.format(context.message.author.mention),
        'Весь мир вертится вокруг тебя, {} :earth_asia:'.format(context.message.author.mention),
        'За тобой выехали, {} :spy:'.format(context.message.author.mention),
        'Сегодня повезёт, {} :four_leaf_clover:'.format(context.message.author.mention),
        'Сегодня забухаем в :poop:, {}'.format(context.message.author.mention),
        'Мне нечего тебе сказать, {} :robot:'.format(context.message.author.mention),
    ]
    await bot.say(random.choice(possible_responses))