from fastapi import APIRouter

router = APIRouter()

@router.post("/", summary="占卜")
async def divination():
    return {"message": "Divination"}
