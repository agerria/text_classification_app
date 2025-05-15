import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis import Redis
from rq import Queue

from sqladmin import Admin

from .db import Base, engine

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

admin = Admin(app, engine)

redis = Redis.from_url(os.getenv("REDIS_URL"))
task_queue = Queue("tasks", connection=redis, default_timeout=60*60)

from .views import *

from .models import *
Base.metadata.create_all(bind=engine)
