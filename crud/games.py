from core.db import DB_CONN_STRING
import asyncpg

async def get_game(app_id):
    connection: asyncpg.Connection = \
        await asyncpg.connect(DB_CONN_STRING)
    
    game = await connection.fetchrow(
        'SELECT * FROM games WHERE app_id = $1',
        app_id
    )
    
    await connection.close()    
    
    return game

async def get_all_games():
    connection: asyncpg.Connection = \
        await asyncpg.connect(DB_CONN_STRING)
    
    games = await connection.fetch(
        'SELECT * FROM games'
    )
    
    await connection.close()
    
    if not len(games):
        return None
    
    games = [dict(game) for game in games]
    
    return games

async def insert_game(game: dict, has_achievements: bool):
    connection: asyncpg.Connection = \
        await asyncpg.connect(DB_CONN_STRING)
    
    await connection.execute(
        """
        INSERT INTO games (app_id, name, last_modified, has_acheievements)
        VALUE ($1, $2, $3, $4)
        """,
        game['app_id'],
        game['name'],
        game['last_modified'],
        has_achievements
    )
    
    connection.close()

async def update_last_modified(app_id, last_modified):
    connection: asyncpg.Connection = \
        await asyncpg.connect(DB_CONN_STRING)

    await connection.execute(
        """
        UPDATE games
        SET last_modified = $1
        WHERE app_id = $2
        """,
        last_modified,
        app_id
    )
    
    connection.close()
    
async def update_has_achievements(app_id, has_achievements):
    connection: asyncpg.Connection = \
    await asyncpg.connect(DB_CONN_STRING)

    await connection.execute(
        """
        UPDATE games
        SET has_acheievements = $1
        WHERE app_id = $2
        """,
        has_achievements,
        app_id
    )
    
    connection.close()
        
async def db_has_games() -> bool:
    connection: asyncpg.Connection = \
        await asyncpg.connect(DB_CONN_STRING)
    
    result = await connection.execute('SELECT * FROM games')
    has_games = int(result.split(' ')[1])
    
    connection.close()
    
    return bool(has_games)