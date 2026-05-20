from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from app.client import stream_ollama
from app.logger import get_logger
from app.service import generate_stream, generate_text

logger = get_logger()
router = APIRouter()


@router.get("/health")
async def health():
    return {"status": "ok"}


@router.post("/generate-text")
async def generate_text_route(payload: dict):
    prompt = payload.get("prompt")
    logger.info(f"Prompt received: {prompt}")
    if not prompt:
        raise HTTPException(status_code=400, detail="Prompt required")

    try:
        output = await generate_text(prompt)
        return {"output": output}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/generate-stream")
async def generate_stream_route(prompt: str):
    async def event_generator():
        async for item in generate_stream(prompt):

            yield f"data: {item['token']}\n\n"

            if item["done"]:
                yield "data: [DONE]\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
