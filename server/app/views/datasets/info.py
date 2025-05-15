from fastapi import Depends
from fastapi_utils.cbv import cbv

from sqlalchemy import func


from . import router
from app.auth import AuthView

from app.models import Dataset, DatasetRow
from app.shema.dataset import (
    SDatasetInfo, 
    SDatasetClass, 
    SDatasetRowTableRow,
    SDatasetRowTable,
)
from app.shema.table import STableOptions


@cbv(router)
class DatasetInfoView(AuthView):
    @router.get('/{id}')
    async def info(self, id:int) -> SDatasetInfo:
        dataset = (
            self.db.query(Dataset)
            .filter(Dataset.id == id)
            .scalar()
        )
        
        info = SDatasetInfo.from_orm(dataset)
        
        rows_count = self.db.query(
            func.count(DatasetRow.num)
            .filter(DatasetRow.dataset_id == dataset.id)
        ).scalar()
        
        classes = (
            self.db.query(
                DatasetRow.classname.label('name'),
                func.count(DatasetRow.num).label('rows_count'),
                (func.count(DatasetRow.num) * 100 / rows_count).label('percent'),
            )
            .filter(
                DatasetRow.dataset_id == dataset.id
            )
            .group_by(
                DatasetRow.classname
            )
            .order_by(
                func.count(DatasetRow.num).label('rows_count').desc(),
            )
        )
        
        info.rows_count = rows_count
        info.classes = [
            SDatasetClass(**cls._asdict())
            for cls in classes
        ]
        
        return info
    
    @router.get('/{id}/table')
    async def rows_table(self, id:int, options: STableOptions = Depends()):
        rows = (
            self.db.query(DatasetRow)
            .filter(DatasetRow.dataset_id == id)
            .order_by(DatasetRow.num)
        )
        
        total = rows.count()
        data = [
            SDatasetRowTableRow.from_orm(row)
            for row in rows.offset(options.offset).limit(options.limit)
        ]
        
        return SDatasetRowTable(data=data, total=total)
        
        
        
        
    