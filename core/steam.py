import requests
from . import settings

BASE_URL = 'https://api.steampowered.com'
GET_APP_LIST_URL = BASE_URL + '/IStoreService/GetAppList/v1/'
GET_SCHEMA_FOR_GAME_URL = BASE_URL + '/ISteamUserStats/GetSchemaForGame/v2/'
GET_PLAYER_SUMMARY_URL = BASE_URL + '/ISteamUser/GetPlayerSummaries/v2/'
GET_PLAYER_ACHEIVEMENTS_URL = BASE_URL + '/ISteamUserStats/GetPlayerAchievements/v1/'

def fetch_games():
    params = {
        'key': settings.STEAM_API_KEY,
        'include_games': 'true',
        'include_dlc': 'false',
        'include_software': 'false',
        'max_results': '50000',
    }
    
    response = requests.get(
        GET_APP_LIST_URL, params=params
    ).json()['response']
    
    games = response['apps']
    
    while 'last_appid' in response:
        params['last_appid'] = response['last_appid']
        
        response = requests.get(
            GET_APP_LIST_URL, params=params
        ).json()['response']
        
        games.extend(response['apps'])
    
    parsed_games = []
    
    for app in games:
        parsed_games.append({
            'app_id': app['appid'],
            'name': app['name'],
            'last_modified': app['last_modified']
        })
        
    return parsed_games
        
def fetch_achievements(app_id):
    params = {
        'key': settings.STEAM_API_KEY,
        'appid': str(app_id)
    }
    
    try:
        response = requests.get(
            GET_SCHEMA_FOR_GAME_URL, 
            params=params
        ).json()['game']['availableGameStats']['achievements']
    except KeyError:
        return None
    
    return response

def fetch_player_summary(steam_id):
    params = {
        'key': settings.STEAM_API_KEY,
        'steamids': steam_id
    }
    
    response = requests.get(
        GET_PLAYER_SUMMARY_URL, 
        params=params
    ).json()['response']['players'][0]

    if not response:
        return None
    
    return response
    
def fetch_player_achievements(steam_id, app_id):
    params = {
        'key': settings.STEAM_API_KEY,
        'steam_id': steam_id,
        'appid': app_id
    }
    
    response = requests.get(
        GET_PLAYER_ACHEIVEMENTS_URL,
        params=params
    ).json()['playerstats']['achievements']
    
    if not response:
        return None
    
    return response
        