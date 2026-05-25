from app.common.logger import get_logger
from app.common.state import active_requests
from app.integration.client import stream_ollama
from app.queue.queue import request_queue

NUM_WORKERS = 2  # start with 2–5 depending on CPU/RAM


logger = get_logger()


async def worker(worker_id: int):
    logger.info(f"Worker-{worker_id} started")

    while True:
        req = await request_queue.get()

        try:
            logger.info(f"Worker-{worker_id} picked request: {req.prompt}")

            async for chunk in stream_ollama(req.prompt):
                if not active_requests.get(req.request_id, True):
                    logger.info(f"Worker-{worker_id}: cancelled")
                    break

                token = chunk.get("response", "")
                done = chunk.get("done", False)

                await req.response_queue.put(token)

                if done:
                    await req.response_queue.put("[DONE]")
                    break

        except Exception as e:
            await req.response_queue.put(f"[ERROR] {str(e)}")

        finally:
            request_queue.task_done()
