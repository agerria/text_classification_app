from sqlalchemy import text
from sqlalchemy.orm import Session

from app.models import Dataset

class DatasetSplitter:
    def __init__(self, session: Session, dataset_id: int):
        self.session = session
        self.dataset_id = dataset_id
        self.dataset: Dataset = (
            session.query(Dataset)
            .filter(Dataset.id == dataset_id)
            .scalar()
        )

    def split(self) -> None:
        n = self.dataset.fold_count
        self._random_split(n)
        self._stratified_split(n)
        
        self.session.commit()

    def _random_split(self, n: int) -> None:
        query = text("""
            UPDATE dataset_row
            SET random_fold = ((sub.rn - 1) % :n) + 1
            FROM (
                SELECT num, ROW_NUMBER() OVER (ORDER BY random()) AS rn
                FROM dataset_row
                WHERE dataset_id = :dataset_id
            ) AS sub
            WHERE dataset_row.num = sub.num AND dataset_row.dataset_id = :dataset_id
        """)
        self.session.execute(query, {'n': n, 'dataset_id': self.dataset_id})

    def _stratified_split(self, n: int) -> None:
        query = text("""
            WITH ranked AS (
                SELECT 
                    num,
                    ROW_NUMBER() OVER (
                        PARTITION BY classname 
                        ORDER BY random()
                    ) AS rn
                FROM dataset_row
                WHERE dataset_id = :dataset_id
            )
            UPDATE dataset_row
            SET stratified_fold = ((ranked.rn - 1) % :n) + 1
            FROM ranked
            WHERE 
                dataset_row.num = ranked.num 
                AND dataset_row.dataset_id = :dataset_id
        """)
        self.session.execute(query, {'n': n, 'dataset_id': self.dataset_id})