from app.client import stream_ollama
from app.queue import request_queue


async def worker():
    print("Worker started...")

    while True:
        req = await request_queue.get()

        try:
            async for chunk in stream_ollama(req.prompt):
                if req.cancelled:
                    print("Request cancelled, stopping worker early")
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
