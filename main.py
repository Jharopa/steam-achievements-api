from contextlib import asynccontextmanager

import asyncpg
from fastapi import FastAPI, HTTPException
from redis import Redis
from rq import Queue

from core import steam
from core.db import DB_CONN_STRING
import crud
import tasks

@asynccontextmanager
async def lifespan(app: FastAPI):
    connection: asyncpg.Connection = await asyncpg.connect(DB_CONN_STRING)
    
    await connection.execute(open('./sql/schema.sql', 'r').read())
    
    redis_conn = Redis(host="redis")
    queue = Queue(connection=redis_conn)
    
    queue.enqueue(
        tasks.data.fetch_and_save, 
        job_timeout=(60 * 60 * 24 * 28),
    )
    
    yield
    
app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Achievements"}

@app.get("/games/{app_id}")
async def read_item(app_id: int):
    game = await crud.games.get_game(app_id)
        
    if game is None:
        raise HTTPException(status_code=404, detail=f"App ID {app_id} does not exist")
    
    return game

@app.get("/games/achievements/{app_id}")
async def read_achievemnts(app_id: int):
    achievements = await crud.achievements.get_achievements(app_id)
    
    if achievements is None:
        achievements = steam.fetch_achievements(app_id)
        
        if achievements is None: 
            raise HTTPException(
                status_code=404, detail=f"Achievements for App ID {app_id} do not exist"
            )
        
        await crud.achievements.insert_achievements(app_id, achievements)
        
    return achievements
