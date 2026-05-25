import asyncio

import dotenv
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.queue.worker import NUM_WORKERS, worker
from app.routers import common, stream, stream_queue

app = FastAPI()
dotenv.load_dotenv()

# API routes
app.include_router(common.router)
app.include_router(stream.router)
app.include_router(stream_queue.router)

# Serve UI
app.mount("/ui", StaticFiles(directory="ui"), name="ui")


# Optional: root route → open UI directly
@app.get("/")
async def root():
    return FileResponse("ui/index.html")


@app.on_event("startup")
async def startup():
    for i in range(NUM_WORKERS):
        asyncio.create_task(worker(i))
