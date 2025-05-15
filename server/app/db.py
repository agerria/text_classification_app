from .config import Config

from typing import List
from fastapi import Depends

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session, Query

from .shema.base import OrmModel

engine = create_engine(Config.SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Base = declarative_base()
class Base(DeclarativeBase):
    pass



class DBView:
    db: Session = Depends(get_db)
    
    
    def query_to_schemas(self, Schema: OrmModel, query: Query) -> List[OrmModel]:
        return [
            Schema.from_orm(obj)
            for obj in query
        ]
            
    
    