import uuid
from fastapi import Depends
from fastapi_utils.cbv import cbv


from . import router
from app.auth import AuthView
from app.models import Task

from app import task_queue
from app.tasks import long_cpu_task


@cbv(router)
class TestTaskView(AuthView):
    @router.post("/start")
    def start_task(self):
        # Создаем запись в БД
        task = Task(
            job_id=str(uuid.uuid4()),
            status="queued",
            task_type="cpu_task"
        )
        self.db.add(task)
        self.db.commit()
        
        # Ставим задачу в очередь
        job = task_queue.enqueue(long_cpu_task, job_id=task.job_id)
        task.job_id = job.id
        self.db.commit()
        
        return {"job_id": job.id}

    @router.get("/list")
    def get_tasks(self):
        return self.db.query(Task).all()