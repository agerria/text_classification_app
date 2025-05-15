import numpy as np
from pathlib import Path

from sqlalchemy import func, and_
from sqlalchemy.orm import Session

from app.models.dataset_data import DatasetRow
from app.logic.fold.consts import FoldType

from .base import BaseTraslator


class DBDatasetFoldTraslator(BaseTraslator):
    def __init__(self, db: Session, dataset_id: int):
        self.db = db
        self.dataset_id = dataset_id

        self.classes = []
        self.texts = []
        self.test_count = 0

    def load_data(self, fold_type: FoldType, fold_num: int):
        query = self.db.query(
            DatasetRow.classname,
            DatasetRow.text,
        ).filter(
            DatasetRow.dataset_id == self.dataset_id
        )

        # Определение условий для фолдов
        fold_column = getattr(DatasetRow, f"{fold_type.value}_fold")
        test_query = query.filter(fold_column == fold_num).order_by(DatasetRow.num)
        train_query = query.filter(fold_column != fold_num).order_by(DatasetRow.num)
        
        test_rows = test_query.all()
        train_rows = train_query.all()
        
        self.test_count = len(test_rows)
        all_rows = test_rows + train_rows

        # Заполнение данных
        self.classes = np.array([row.classname for row in all_rows])
        self.texts = [row.text for row in all_rows]

        # Очистка сессии
