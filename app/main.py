from fastapi import FastAPI
import uvicorn
from app.routers.health_check import router as health_check_router
from app.routers.check_db_connection import router as check_db_connection_router
from app.routers.check_redis_connection import router as check_redis_connection_router
from app.core.config import settings
from app.routers.user import router as user
from app.routers.company import router as company


app = FastAPI()
app.include_router(health_check_router)
app.include_router(check_db_connection_router)
app.include_router(check_redis_connection_router)
app.include_router(user)
app.include_router(company)


if __name__ == "__main__":
    uvicorn.run('app.main:app', host=settings.HOST, port=settings.PORT, reload=settings.RELOAD)
