from fastapi import FastAPI
import uvicorn
from app.routers.health_check import router as health_check_router
from app.routers.check_db_connection import router as check_db_connection_router
from app.core.config import settings


app = FastAPI()
app.include_router(health_check_router)
app.include_router(check_db_connection_router)


if __name__ == "__main__":
    uvicorn.run('app.main:app', host=settings.HOST, port=settings.PORT, reload=settings.RELOAD)
