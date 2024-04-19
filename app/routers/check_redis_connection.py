from fastapi import APIRouter
from redis import asyncio as aioredis
from app.core.config import settings
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/connect/redis/")
async def check_redis_connect():
    try:
        redis_pool = await aioredis.from_url(settings.REDIS_URL, decode_responses=True)
        return JSONResponse({"status": "OK", "message": "Connected to Redis database"})
    except Exception as e:
        logger.error(f"Failed to connect to Redis database: {str(e)}")
        return JSONResponse({"status": 500, "error_message": str(e)})


