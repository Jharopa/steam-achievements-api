import asyncio
import datetime

import asyncpg

from core import steam
from core.db import DB_CONN_STRING
from crud.achievements import insert_achievements
from crud.games import (
    get_game, 
    insert_game, 
    update_has_achievements, 
    update_last_modified,
    db_has_games
)

async def fetch_and_save():
    connection: asyncpg.Connection = \
        await asyncpg.connect(DB_CONN_STRING)
    
    has_games = await db_has_games()
    
    api_games = steam.fetch_games()
    
    needs_achievements = []
    
    if not has_games:
        for game in api_games:
            await insert_game(game, False)
            
            needs_achievements.append(game['app_id'])
    else:
        for game in api_games:
            game_db = await get_game(game['app_id'])
            
            if game_db is None:
                await insert_game(game, False)
                needs_achievements.append(game['app_id'])
            elif game['last_modified'] != game_db['last_modified']:
                await update_last_modified(game['app_id'], game['last_modified'])
                needs_achievements.append(game['app_id'])
    
    for game in needs_achievements:
        try:
            print(f'{game["name"]} achievements requested at {datetime.datetime.now()}')
            achievements = steam.fetch_achievements(game['app_id'])
        except Exception as e:
            print(f'Error, skipping acheivements fetch for {game["name"]}')
            print(repr(e))
            
        if achievements:    
            try:
                print(f'Adding {game["name"]} achievements to database')
                print(f'{achievements}')
                await insert_achievements(game['app_id'], achievements)
                await update_has_achievements(game['app_id'], True)
            except Exception as e:
                print(f'Error, skipping acheivements insertion for {game["name"]}')
                print(repr(e))
        else:
            try:
                await update_has_achievements(game['app_id'], False)
            except Exception as e:
                print(f'Error, updating {game["name"]} has_achievement status')
                print(repr(e))
        
        await asyncio.sleep(5)
    
    await connection.close()
