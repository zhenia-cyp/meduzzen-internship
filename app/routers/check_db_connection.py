from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from app.db.database import get_async_session
from fastapi.responses import JSONResponse
from sqlalchemy import text
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/connect/db/")
async def check_db_connection(session: AsyncSession = Depends(get_async_session)):
    try:
        await session.execute(text("SELECT 1"))
        return JSONResponse({"status": "OK", "message": "Connected to database"})
    except Exception as e:
        logger.error(f"Failed to connect to Redis database: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to connect to the database: {str(e)}")



