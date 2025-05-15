from fastapi import  APIRouter
from app import app

router = APIRouter(prefix='/comparison', tags=['Сравнение'])

from .table import ComparisonTableView
from .report import ComparisonReportView

app.include_router(router)