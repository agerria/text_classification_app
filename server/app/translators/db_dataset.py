import numpy as np
from pathlib import Path

from sqlalchemy import func, and_
from sqlalchemy.orm import Session

from app.models.dataset_data import DatasetRow

from .base import BaseTraslator


class DBDatasetTraslator(BaseTraslator):
    def __init__(self, db: Session, dataset_id: int):
        self.db = db
        self.dataset_id = dataset_id

        self.classes = []
        self.texts = []

    def load_data(self):
        rows = (
            self.db.query(
                DatasetRow.classname,
                DatasetRow.text,
            ).filter(
                DatasetRow.dataset_id == self.dataset_id,
            ).order_by(
                DatasetRow.num
            )
        )
        
        for name, text in rows:
            self.classes.append(name)
            self.texts.append(text)

        self.classes = np.array(self.classes)
        del self.db
