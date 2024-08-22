from fastapi import FastAPI
from app.api.v1.endpoints import (
    message
)

app = FastAPI()

api_prefix = "/api/v1"

app.include_router(message.router, prefix=api_prefix, tags=["Message Analayzer"])
