from os import environ

from beanie import init_beanie
from dotenv import load_dotenv
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from schemas import User, Teacher
from routes import users, teachers

load_dotenv() # noqa

app = FastAPI()
app.include_router(users.router)
app.include_router(teachers.router)

@app.on_event("startup")
async def start():
    db_client = AsyncIOMotorClient(environ["MONGODB_URL"])
    await init_beanie(database=db_client.movs, document_models=[User, Teacher])
