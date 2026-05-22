import httpx

from app.integration.client import call_ollama, stream_ollama
from app.common.logger import get_logger

logger = get_logger()


async def generate_text(prompt: str):
    logger.info(f"Prompt received: {prompt}")
    try:
        result = await call_ollama(prompt, timeout=60.0)
    except httpx.TimeoutException:
        return {"error": "LLM timeout"}
    return result.get("response", "")


async def generate_stream(prompt: str):
    async for chunk in stream_ollama(prompt):
        token = chunk.get("response", "")
        done = chunk.get("done", False)

        yield {"token": token, "done": done}

        if done:
            break
