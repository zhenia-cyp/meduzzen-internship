from fastapi import APIRouter
from redis import asyncio as aioredis
from app.core.config import settings
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/connect/redis/")
async def check_redis_connect():
    try:
        redis_pool = await aioredis.from_url(settings.REDIS_URL, decode_responses=True)
        return JSONResponse({"status": "OK", "message": "Connected to Redis database"})
    except Exception as e:
        return JSONResponse({"status": 500, "error_message": str(e)})


