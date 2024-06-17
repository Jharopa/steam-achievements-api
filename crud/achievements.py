import asyncpg

from core.db import DB_CONN_STRING


async def get_achievements(app_id):
    connection = await asyncpg.connect(DB_CONN_STRING)

    achievments = await connection.fetch(
        "SELECT * FROM achievements WHERE app_id = $1", app_id
    )

    await connection.close()

    if not len(achievments):
        return None

    achievments = [dict(achievement) for achievement in achievments]

    return achievments


async def insert_achievements(app_id, achievements):
    connection = await asyncpg.connect(DB_CONN_STRING)

    for achievement in achievements:
        await connection.execute(
            """
            INSERT INTO achievements (
                name,
                app_id,
                display_name,
                description,
                icon_url,
                icon_url_gray,
                hidden
            )
            VALUES ($1, $2, $3, $4, $5, $6, $7)
            """,
            achievement["name"],
            int(app_id),
            achievement["displayName"],
            achievement.get("description", None),
            achievement["icon"],
            achievement["icongray"],
            bool(achievement["hidden"]),
        )

    await connection.close()
