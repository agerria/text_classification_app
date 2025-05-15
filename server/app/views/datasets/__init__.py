from fastapi import  APIRouter
from app import app

router = APIRouter(prefix='/datasets', tags=['Датасеты'])

from .table import DatasetsTableView
from .info import DatasetInfoView

app.include_router(router)