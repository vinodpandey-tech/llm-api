import asyncio

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.common.logger import get_logger
from app.common.models import GenerateRequest, QueueRequest
from app.common.state import active_requests
from app.queue.queue import request_queue

logger = get_logger()
router = APIRouter()


@router.post("/generate-stream-queued")
async def generate_stream_queued_route(generateRequest: GenerateRequest):
    logger.info(f"API /generate-stream-queued invoked with request: {generateRequest}")
    return await process_request(generateRequest.prompt, generateRequest.request_id)


## Added only for UI tests
@router.get("/generate-stream-queued")
async def generate_stream_queued_ui_route(prompt: str, request_id: str):
    logger.info(f"UI test /generate-stream-queued invoked with request: {prompt}")
    return await process_request(prompt, request_id)


async def process_request(prompt: str, request_id: str):
    if request_queue.full():
        return StreamingResponse(
            iter([b"data: [ERROR] Server busy\n\n"]), media_type="text/event-stream"
        )

    active_requests[request_id] = True
    response_queue = asyncio.Queue()
    req = QueueRequest(
        prompt=prompt, response_queue=response_queue, request_id=request_id
    )

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
                continue

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )
