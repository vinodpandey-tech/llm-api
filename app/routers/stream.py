from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.logger import get_logger
from app.models import GenerateRequest
from app.service import generate_stream
from app.state import active_requests

logger = get_logger()
router = APIRouter()


@router.post("/generate-stream")
async def generate_stream_route(generateRequest: GenerateRequest):
    logger.info(f"API /generate-stream invoked with request: {generateRequest}")
    return await process_request(generateRequest.prompt, generateRequest.request_id)


@router.get("/generate-stream")
async def generate_stream_ui_route(prompt: str, request_id: str):
    logger.info(f"UI test /generate-stream invoked with request: {prompt}")
    return await process_request(prompt, request_id)


async def process_request(prompt: str, request_id: str):
    active_requests[request_id] = True

    async def event_generator():
        try:
            async for item in generate_stream(prompt):
                if not active_requests.get(request_id, True):
                    logger.info("Request cancelled explicitly")
                    break

                yield f"data: {item['token']}\n\n"

                if item["done"]:
                    logger.info(f"Completed response for prompt: {prompt}")
                    yield "data: [DONE]\n\n"
                    break

        except Exception as e:
            logger.exception("Streaming error")
            yield f"data: [ERROR] {str(e)}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )
