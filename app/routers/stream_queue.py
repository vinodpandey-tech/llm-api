import asyncio

from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

from app.logger import get_logger
from app.models import GenerateRequest, QueueRequest
from app.queue import request_queue

logger = get_logger()
router = APIRouter()


@router.post("/generate-stream-queued")
async def generate_stream_queued_route(
    request: Request, generateRequest: GenerateRequest
):
    logger.info(f"API /generate-stream-queued invoked with request: {generateRequest}")
    return await process_request(request, generateRequest.prompt)


## Added only for UI tests
@router.get("/generate-stream-queued")
async def generate_stream_queued_ui_route(request: Request, prompt: str):
    logger.info(f"UI test /generate-stream-queued invoked with request: {prompt}")
    return await process_request(request, prompt)


async def process_request(request: Request, prompt: str):
    response_queue = asyncio.Queue(maxsize=100)

    req = QueueRequest(prompt=prompt, response_queue=response_queue)

    # enqueue request
    await request_queue.put(req)

    async def event_generator():
        while True:
            try:
                token = await asyncio.wait_for(response_queue.get(), timeout=1.0)

                if token == "[DONE]":
                    logger.info(f"Completed response for prompt: {prompt}")
                    yield "data: [DONE]\n\n"
                    break

                if token.startswith("[ERROR]"):
                    yield f"data: {token}\n\n"
                    break

                yield f"data: {token}\n\n"

            except asyncio.TimeoutError:
                if await request.is_disconnected():
                    logger.info("Client disconnected → stopping stream")
                    req.cancelled = True
                    break
                continue

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )
