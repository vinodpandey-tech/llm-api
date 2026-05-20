import httpx

from app.client import call_ollama
from app.logger import get_logger

logger = get_logger()


async def generate_text(prompt: str):
    logger.info(f"Prompt received: {prompt}")
    try:
        result = await call_ollama(prompt, timeout=60.0)
    except httpx.TimeoutException:
        return {"error": "LLM timeout"}
    return result.get("response", "")
