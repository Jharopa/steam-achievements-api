from fastapi import APIRouter, HTTPException

import crud.games

router = APIRouter()


@router.get("/games/{app_id}")
async def read_item(app_id: int):
    try:
        game = await crud.games.get_game(app_id)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database retrieval failed with exception: {repr(e)}",
        )

    if game is None:
        raise HTTPException(status_code=404, detail=f"App ID {app_id} does not exist")

    return game
