from fastapi import  APIRouter
from app import app

router = APIRouter(prefix='/classification', tags=['Классификация'])

from .fabric import ClassificationView

app.include_router(router)