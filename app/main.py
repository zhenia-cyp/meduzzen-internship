from fastapi import FastAPI
from routers.first_route import router

app = FastAPI()
app.include_router(router)