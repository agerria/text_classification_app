from fastapi import Depends
from fastapi_utils.cbv import cbv

from sqlalchemy import func

from . import router
from app.auth import AuthView

from app.shema.table import STableOptions
from app.shema.dataset import SDatasetTableRow, SDatasetTable

from app.models import (
    Dataset,
    DatasetRow,
)

@cbv(router)
class DatasetsTableView(AuthView):
    @router.get('/table')
    async def table(self, options: STableOptions = Depends()) -> SDatasetTable:
        class_count_subquery = (
            self.db.query(
                DatasetRow.dataset_id,
                func.count(func.distinct(DatasetRow.classname)).label("class_count")
            )
            .group_by(DatasetRow.dataset_id)
            .subquery()
        )

        datasets_query = (
            self.db.query(
                Dataset.id,
                Dataset.name,
                Dataset.description,
                func.count(Dataset.rows).label("rows_count"),
                func.coalesce(class_count_subquery.c.class_count, 0).label("class_count")
            )
            .outerjoin(class_count_subquery, Dataset.id == class_count_subquery.c.dataset_id)
            .outerjoin(Dataset.rows)
            .group_by(Dataset.id, Dataset.name, Dataset.description, class_count_subquery.c.class_count)
            .offset(options.offset)
            .limit(options.limit)
        )

        total = self.db.query(func.count(Dataset.id)).scalar()

        data = [
            SDatasetTableRow(
                id=dataset.id,
                name=dataset.name,
                description=dataset.description,
                class_count=dataset.class_count,
                rows_count=dataset.rows_count
            )
            for dataset in datasets_query
        ]

        return SDatasetTable(data=data, total=total)