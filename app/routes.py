from fastapi import APIRouter, HTTPException

from app.logger import get_logger
from app.service import generate_text

logger = get_logger()

router = APIRouter()


@router.get("/health")
async def health():
    return {"status": "ok"}


@router.post("/generate")
async def generate(payload: dict):
    prompt = payload.get("prompt")
    logger.info(f"Prompt received: {prompt}")
    if not prompt:
        raise HTTPException(status_code=400, detail="Prompt required")

    try:
        output = await generate_text(prompt)
        return {"output": output}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
