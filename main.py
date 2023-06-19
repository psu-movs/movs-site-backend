from os import environ

from beanie import init_beanie
from dotenv import load_dotenv
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.middleware.cors import CORSMiddleware

from schemas import User, Teacher, DepartmentHead, DepartmentInfo, Article, ScienceWork, ApplicantsCompany
from routes import users, teachers, department_info, news, science_works, applicants

load_dotenv()

app = FastAPI(
    title="КафедраМОВС",
)
app.include_router(users.router)
app.include_router(teachers.router)
app.include_router(department_info.router)
app.include_router(news.router)
app.include_router(science_works.router)
app.include_router(applicants.router)


@app.on_event("startup")
async def start():
    db_client = AsyncIOMotorClient(environ["MONGODB_URL"])
    await init_beanie(database=db_client.movs, document_models=[User, Teacher, DepartmentHead, DepartmentInfo, Article, ScienceWork, ApplicantsCompany])


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["Content-Type", "Authorization"],
)