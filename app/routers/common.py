from fastapi import APIRouter, HTTPException

from app.logger import get_logger
from app.models import GenerateRequest
from app.service import generate_text
from app.state import active_requests

logger = get_logger()
router = APIRouter()


@router.get("/health")
async def health():
    return {"status": "ok"}


@router.post("/cancel")
async def cancel(request_id: str):
    active_requests[request_id] = False


@router.post("/generate-text")
async def generate_text_route(generateRequest: GenerateRequest):
    logger.info("API /generate-text invoked with request", generateRequest)

    try:
        output = await generate_text(generateRequest.prompt)
        return {"output": output}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
