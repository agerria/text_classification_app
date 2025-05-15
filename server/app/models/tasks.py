import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from sqladmin import ModelView
from app.db import Base

class Task(Base):
    __tablename__ = 'tasks'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    job_id: Mapped[str] 
    status: Mapped[str] 
    task_type: Mapped[str]


class TaskAdmin(ModelView, model=Task):
    column_list = [Task.id, Task.job_id, Task.status, Task.task_type]
    column_searchable_list = [Task.job_id]
    column_sortable_list = [Task.id]
    form_columns = [Task.job_id, Task.status, Task.task_type]