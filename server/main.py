from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from app.db.base import Base
from app.db.session import engine
from app.api.v1.endpoints import (
    message
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        async with engine.begin() as conn:
            # print("Database connection successful!")
            await conn.run_sync(Base.metadata.create_all)
    except Exception as e:
        print(f"Failed to connect to the database: {e}")
    yield

UPLOAD_DIRECTORY = "uploaded_files"

app = FastAPI(lifespam=lifespan)

api_prefix = "/api/v1"

app.mount("/files", StaticFiles(directoyr=UPLOAD_DIRECTORY), name="files")

app.include_router(message.router, prefix=api_prefix, tags=["message"])
