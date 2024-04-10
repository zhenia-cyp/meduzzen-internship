from fastapi import FastAPI
import uvicorn
from app.routers.health_check import router
from app.core.config import Settings

app = FastAPI()
app.include_router(router)

settings = Settings()

if __name__ == "__main__":
    uvicorn.run(app, host=settings.HOST, port=settings.PORT, debug=settings.DEBUG)