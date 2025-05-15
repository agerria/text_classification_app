from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from fastapi_utils.cbv import cbv

from sqlalchemy import insert

from datetime import datetime
from pathlib import Path

import pandas as pd

from app import app
from app.auth import AuthView
from app.shema.base import BaseModel
from app.shema.dataset import SDatasetAdd

from app.models import Dataset, DatasetRow
from app.logic.fold.dataset_spliter import DatasetSplitter

router = APIRouter(prefix='/upload', tags=['Загрузка файлов'])

UPLOAD_DIR = Path('app/upload')

class SFile(BaseModel):
    value: str
    label: str
    
class SFileHeaders(BaseModel):
    headers: list[str]




@cbv(router)
class Upload(AuthView):
    @router.post('/')
    async def upload(self, file: UploadFile = File(...)) -> SFile:
        filename = file.filename
        file_path = self.file_path(filename)
        try:
            contents = file.file.read()
            with open(file_path, 'wb') as f:
                f.write(contents)
        except Exception:
            raise HTTPException(status_code=500, detail='Ошибка при сохранении файла')
        finally:
            file.file.close()

        return SFile(value=filename, label=filename)
    
    
    @router.get('/list/')
    async def list(self) -> list[SFile]:
        files = [
            SFile(value=file.name, label=file.name)
            for file in UPLOAD_DIR.iterdir()
            if file.is_file()
        ]
        # print(files)
        return files
    
    
    @router.get('/headers/')
    async def headers(self, filename: str, separator: str) -> SFileHeaders:
        print(f'{filename=}')
        print(f'{separator=}')
        return self.get_headers(filename, separator)
        
    
    
    @router.post('/add/')
    async def add(self, info: SDatasetAdd):
        dataset = Dataset(**info.dict())
        self.db.add(dataset)
        self.db.commit()
        
        df = pd.read_csv(
            self.file_path(dataset.file), 
            sep=dataset.separator, 
            usecols=[dataset.class_header, dataset.data_header]
        )
        
        rows = [
            {
                'dataset_id': dataset.id,
                'num': index + 1,
                'classname': row[dataset.class_header],
                'text': row[dataset.data_header]
            }
            for index, row in df.iterrows()
        ]
        
        self.db.execute(
            insert(DatasetRow),
            rows
        )
        self.db.commit()
        
        return {}
    
    
    @classmethod
    def file_path(cls, filename):
        return UPLOAD_DIR / Path(filename)
    
    
    def get_headers(self, filename: Path, separator: str) -> SFileHeaders:
        try:
            # with open(self.file_path(filename), newline='', encoding='utf-8') as f:
            #     reader = csv.reader(f, delimiter=separator)
            #     headers = next(reader) 
            df = pd.read_csv(self.file_path(filename), sep=separator, nrows=0)
            headers = df.columns.tolist()
        except Exception:
            raise HTTPException(status_code=400, detail='Ошибка при чтении заголовков из файла')
        
        return SFileHeaders(headers=headers)
    


    @router.post('/reset-folds/{dataset_id}')
    def reset_folds(self, dataset_id: int):
        splitter = DatasetSplitter(self.db, dataset_id)
        splitter.split()
        return {}
    


app.include_router(router)