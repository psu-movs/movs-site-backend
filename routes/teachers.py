import aiohttp
from fastapi import APIRouter

from config import API_PREFIX

router = APIRouter(prefix=API_PREFIX)
session: aiohttp.ClientSession | None = None
TEACHERS_URL = "https://helios.psu.ru/pls/www_psu_ru/teacher_list?p_sdiv_name=%CA%E0%F4%E5%E4%F0%E0%EC%E0%F2%E5%EC%E0%F2%E8%F7%E5%F1%EA%EE%E3%EE%EE%E1%E5%F1%EF%E5%F7%E5%ED%E8%FF%E2%FB%F7%E8%F1%EB%E8%F2%E5%EB%FC%ED%FB%F5%F1%E8%F1%F2%E5%EC"

async def get_session():
    global session
    if session is None or session.closed:
        session = aiohttp.ClientSession()
    return session


@router.get("/teachers")
async def get_list_teachers() -> str:
    # Единственный метод, который возвращает строку и не взаимодействует с бд
    # Изначально это должно было быть во фронте,
    # но спасибо кодировке win1251, которая превращает кириллицу в знаки вопроса
    session = await get_session()
    async with session.get(TEACHERS_URL) as res:
        return await res.text()
