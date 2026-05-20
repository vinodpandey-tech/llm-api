from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.client import stream_ollama
from app.logger import get_logger
from app.service import generate_stream, generate_text

logger = get_logger()
router = APIRouter()


class GenerateRequest(BaseModel):
    prompt: str


@router.get("/health")
async def health():
    return {"status": "ok"}


@router.post("/generate-text")
async def generate_text_route(payload: GenerateRequest):
    prompt = payload.prompt
    logger.info(f"Prompt received: {prompt}")
    if not prompt:
        raise HTTPException(status_code=400, detail="Prompt required")

    try:
        output = await generate_text(prompt)
        return {"output": output}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate-stream")
async def generate_stream_route(request: Request, payload: GenerateRequest):
    prompt = payload.prompt

    async def event_generator():
        async for item in generate_stream(prompt):

            if await request.is_disconnected():
                logger("Client disconnected → stopping stream")
            break

            yield f"data: {item['token']}\n\n"

            if item["done"]:
                yield "data: [DONE]\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")


## Added only for UI tests
@router.get("/generate-stream")
async def generate_stream_route(request: Request, prompt: str):
    async def event_generator():
        async for item in generate_stream(prompt):

            if await request.is_disconnected():
                logger("Client disconnected → stopping stream")
                break

            yield f"data: {item['token']}\n\n"

            if item["done"]:
                yield "data: [DONE]\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
