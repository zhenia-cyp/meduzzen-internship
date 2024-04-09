from fastapi import FastAPI
import uvicorn
from routers.health_check import router
import os


app = FastAPI()
app.include_router(router)

host = os.getenv("HOST")
port = os.getenv("PORT")
debug = os.getenv("DEBUG")

if __name__ == "__main__":
    uvicorn.run(app, host=host, port=port)