import os
import json
import requests
import asyncio

def api_call(api_key, url):
    header = {
            "Authorization": "Bearer {}".format(api_key),
            "Accept": "application/vnd.api+json",
            "Accept-Encoding":"gzip"
            }

    r = requests.get(url, headers=header)
    return r.json()
    # return requests.get(url, headers=header)

def get_player_info(api_key, shard, player_name):
    '''get info about player'''
    url_player = "https://api.pubg.com/shards/{}/players?filter[playerNames]={}".format(shard, player_name)
    player_info = api_call(api_key, url_player)
    try:
        player_id = player_info['data'][0]['id']
    except KeyError:
        player_id = player_info['errors'][0]['title']
    return player_id

def get_season_info(api_key, shard):
    '''get info about current season'''
    url_season = "https://api.pubg.com/shards/{}/seasons".format(shard)
    season_info = api_call(api_key, url_season)
    season_num = len(season_info['data'])
    if season_info['data'][season_num-1]['attributes']['isCurrentSeason']:
        season_id = season_info['data'][season_num-1]['id']
    else:
        season_id = 'Not Found'
    return season_id

def get_general_stat_info(api_key, shard, player_id, season_id,
                            interest_mode, interest_items):
    '''get info about user statistics'''
    url_stat = 'https://api.pubg.com/shards/{}/players/{}/seasons/{}'.format(shard, player_id, season_id)
    general_info = api_call(api_key, url_stat)

    result = {}
    items_dict = {}
    for mode in interest_mode:
        for item in interest_items:
            value = str(general_info['data']['attributes']['gameModeStats'][mode].get(item))
            # add smilies
            if item == 'suicides':
                item += ' :skull:'
            
            items_dict[item] = str(value)
        result[mode] = [items_dict]
    if value:
        return result
    else:
        return 'Not Found'

async def pubg_info(api_key, bot, shard, player_name, interest_mode, interest_items):
    '''collect complex information about player'''
    if player_name is ' ':
        await bot.say('Укажи никнейм')
    else:
        player_id = get_player_info(api_key, shard, player_name)
        if player_id == 'Not Found':
            await bot.say('Такой ник не найден в базе')
        else:
            season_id = get_season_info(api_key, shard)
            if season_id == 'Not Found':
                await bot.say('Актуальный сезон не обнаружен')
            else:
                general_info = get_general_stat_info(api_key, shard, player_id, season_id, interest_mode, interest_items)
                if general_info == 'Not Found':
                    await bot.say('Никнейм найден, актуальный сезон найден, статистика почему-то недоступна :cry:')
                else:
                    for mode in general_info:
                        await bot.say(mode.capitalize() + ':')
                        # bot.say(mode.capitalize() + ':')
                        for key, value in general_info[mode][0].items():
                            await bot.say(key + ' - ' + str(value))
                            # bot.say(key + ' - ' + str(value))
