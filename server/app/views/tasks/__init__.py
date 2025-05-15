from fastapi import  APIRouter
from app import app

router = APIRouter(prefix='/tasks', tags=['Задачи'])

from .test import TestTaskView

app.include_router(router)