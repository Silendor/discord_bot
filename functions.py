import os
import json
import requests

def api_call(url, api_key):
    header = {
            "Authorization": "Bearer {}".format(api_key),
            "Accept": "application/vnd.api+json",
            "Accept-Encoding":"gzip"
            }

    r = requests.get(url, headers=header)
    return r.json()

def get_player_info(shard, player_name, api_key):
    url_player = "https://api.pubg.com/shards/{}/players?filter[playerNames]={}".format(shard, player_name)
    player_info = api_call(url_player, api_key)
    try:
        player_id = player_info['data'][0]['id']
    except KeyError:
        player_id = player_info['errors'][0]['title']
    return player_id

def get_season_info(shard, api_key):
    url_season = "https://api.pubg.com/shards/{}/seasons".format(shard)
    season_info = api_call(url_season, api_key)
    season_num = len(season_info['data'])
    if season_info['data'][season_num-1]['attributes']['isCurrentSeason']:
        season_id = season_info['data'][season_num-1]['id']
    else:
        season_id = 'Not Found'
    return season_id

def get_general_stat_info(shard, player_id, season_id, api_key, 
                            interest_mode, interest_items):
    url_stat = 'https://api.pubg.com/shards/{}/players/{}/seasons/{}'.format(shard, player_id, season_id)
    general_info = api_call(url_stat, api_key)

    result = {}
    items_dict = {}
    for mode in interest_mode:
        for item in interest_items:
            value = general_info['data']['attributes']['gameModeStats'][mode].get(item)
            # add smilies
            if item == 'suicides':
                item += ' :skull:'
            
            items_dict[item] = str(value)
        result[mode] = [items_dict]
    if value:
        return result
    else:
        return 'Not Found'