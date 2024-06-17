from fastapi import APIRouter, HTTPException

import crud.achievements
import core.steam

router = APIRouter()

@router.get("/achievements/{app_id}")
async def read_achievemnts(app_id: int):
    achievements = await crud.achievements.get_achievements(app_id)
    
    if achievements is None:
        achievements = core.steam.fetch_achievements(app_id)
        
        if achievements is None: 
            raise HTTPException(
                status_code=404, detail=f"Achievements for App ID {app_id} do not exist"
            )
        
        await crud.achievements.insert_achievements(app_id, achievements)
        
    return achievements
