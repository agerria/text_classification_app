from fastapi import Depends
from fastapi_utils.cbv import cbv

from sqlalchemy import func

from . import router
from app.auth import AuthView

from app.shema.table import STableOptions
from app.shema.comparison import SCompoarisonTableRow, SComparisonTable
from app.logic.classifications import ClassificationLogic


from app.models import (
    Classification,
    Dataset
)

@cbv(router)
class ComparisonTableView(AuthView):
    @router.get('/table')
    async def table(self, options: STableOptions = Depends()) -> SComparisonTable:
        classifications_query: list[tuple[Classification, Dataset]] = (
            self.db.query(
                Classification,
                Dataset,
            )
            .join(Dataset, Dataset.id == Classification.dataset_id)
            .offset(options.offset)
            .limit(options.limit)
        )

        total = self.db.query(func.count(Classification.hash)).scalar()

        data = [
            # ClassificationLogic.get_settings(self.db, classification=classification)
            SCompoarisonTableRow(
                key = classification.hash,
                hash = classification.hash,
                dataset = dataset.name,
                dataset_id = dataset.id,
                vectorizer = classification.vectorizer,
                classifier = classification.classifier
            )
            for (classification, dataset) in classifications_query
        ]

        return SComparisonTable(data=data, total=total)