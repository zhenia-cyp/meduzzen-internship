import time

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from app.db.database import get_async_session, check_db_connect

router = APIRouter()

@router.get("/")
async def health_check(session: Annotated[AsyncSession, Depends(get_async_session)]):
    await check_db_connect(session)
    return JSONResponse({
      "status_code": 200,
      "detail": "ok",
      "result": "working"
      })




