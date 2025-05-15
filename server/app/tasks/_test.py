# app/tasks.py
import time
from redis import Redis
from rq import get_current_job
from app.db import SessionLocal
from app.models import Task

def fib(n):
    if n <= 1:
        return n
    return fib(n-1) + fib(n-2)

def long_cpu_task():  # ~3 минуты на CPU
    n: int = 50
    job = get_current_job()
    db = SessionLocal()
    
    try:
        task = db.query(Task).filter(Task.job_id == job.id).first()
        task.status = "started"
        db.commit()

        # CPU-bound вычисления
        result = fib(n)
        
        task.status = "finished"
    except Exception as e:
        task.status = f"failed: {str(e)}"
    finally:
        db.commit()
        db.close()
    return result