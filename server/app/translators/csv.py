import numpy as np
import pandas as pd
from pathlib import Path

from .base import BaseTraslator

class CsvTraslator(BaseTraslator):
    def __init__(self, path,  text_column, class_column=None):
        super().__init__(path, text_column, class_column)
    
    
    def load_data(self):
        data = pd.read_csv(self.path)
        self.texts = np.array(data[self.text_column])
        self.classes = np.array(data[self.class_column])
