from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
from app.routers.health_check import router as health_check_router
from app.routers.check_db_connection import router as check_db_connection_router
from app.routers.check_redis_connection import router as check_redis_connection_router
from app.core.config import settings
from app.routers.user import router as user
from app.routers.company import router as company
from app.routers.action import router as action
from app.utils.exceptions import CustomTokenExceptionBase


app = FastAPI()

@app.exception_handler(CustomTokenExceptionBase)
async def token_exception_handler(request: Request, exc: CustomTokenExceptionBase):
    return JSONResponse(
        status_code=401,
        content={"detail": exc.detail},
    )

app.include_router(health_check_router)
app.include_router(check_db_connection_router)
app.include_router(check_redis_connection_router)
app.include_router(user)
app.include_router(company)
app.include_router(action)




if __name__ == "__main__":
    uvicorn.run('app.main:app', host=settings.HOST, port=settings.PORT, reload=settings.RELOAD)
