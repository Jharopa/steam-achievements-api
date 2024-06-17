from contextlib import asynccontextmanager

import asyncpg
from fastapi import FastAPI
from redis import Redis
from rq import Queue

import tasks
from core.db import DB_CONN_STRING
from routers import acheivements, games


@asynccontextmanager
async def lifespan(app: FastAPI):
    connection: asyncpg.Connection = await asyncpg.connect(DB_CONN_STRING)

    await connection.execute(open("./sql/schema.sql", "r").read())

    redis_conn = Redis(host="redis")
    queue = Queue(connection=redis_conn)

    queue.enqueue(
        tasks.data.fetch_and_save,
        job_timeout=(60 * 60 * 24 * 28),
    )

    yield


app = FastAPI(lifespan=lifespan)

app.include_router(games.router)
app.include_router(acheivements.router)


@app.get("/")
async def root():
    return {"message": "Achievements"}
