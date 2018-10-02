import os
import json
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
        player_id = player_info['errors'][0]['title']
    return player_id

@cache.cache('get_season_func', type="file", expire=2592000)
def get_season_info(api_key, shard):
    '''get info about current season'''
    url_season = "https://api.pubg.com/shards/{}/seasons".format(shard)
    # season_id = 'division.bro.official.2018-09'
    season_info = api_call(api_key, url_season)
    season_num = len(season_info['data'])
    if season_info['data'][season_num-1]['attributes']['isCurrentSeason']:
        season_id = season_info['data'][season_num-1]['id']
    else:
        season_id = 'Not Found'
    return season_id

@cache.cache('get_season_func', type="file", expire=300)
def get_general_stat_info(api_key, shard, player_id, season_id,
                            interest_mode, interest_items):
    '''get info about user statistics'''
    url_stat = 'https://api.pubg.com/shards/{}/players/{}/seasons/{}'.format(shard, player_id, season_id)
    general_info = api_call(api_key, url_stat)

    result = {}
    items_dict = {}
    for mode in interest_mode:
        for item in interest_items:
            value = general_info['data']['attributes']['gameModeStats'][mode].get(item)
            # add smilies
            item += add_smile(item)
            items_dict[item] = str(value)
        result[mode] = [items_dict]
    # переделать условие
    if str(value):
        return result
    else:
        return 'Not Found'

async def pubg_info(api_key, bot, shard, player_name, interest_mode, 
                    interest_items, context):
    '''collect complex information about player'''
    if player_name is ' ':
        answer = 'Укажи никнейм, {}'.format(context.message.author.mention)
        await bot.say(answer)
    else:
        player_id = get_player_info(api_key, shard, player_name)
        if player_id == 'Not Found':
            answer = 'Такой ник не найден в базе, {}'.format(context.message.author.mention)
            await bot.say(answer)
        else:
            season_id = get_season_info(api_key, shard)
            if season_id == 'Not Found':
                answer = 'Актуальный сезон не обнаружен'
                await bot.say(answer)
            else:
                general_info = get_general_stat_info(api_key, shard, player_id, 
                                                    season_id, interest_mode, 
                                                    interest_items)
                if general_info == 'Not Found':
                    answer = 'Никнейм найден, актуальный сезон найден, статистика почему-то недоступна :cry:, {}'.format(context.message.author.mention)
                    await bot.say(answer)
                else:
                    for mode in general_info:
                        em_answer = discord.Embed(title=mode.capitalize(), description=player_name, color=0x50bdfe)
                        for key, value in general_info[mode][0].items():
                            em_answer.add_field(name=key, value=value, inline=False)
                    await bot.say(embed=em_answer)

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