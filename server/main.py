from fastapi import FastAPI
from app.api.v1.endpoints import (
    message,
    scheduling
)

app = FastAPI()

api_prefix = "/api/v1"

app.include_router(message.router, prefix=api_prefix, tags=["Message Analayzer"])
app.include_router(scheduling.router, prefix=api_prefix, tags=["Voice Scheduler"])
