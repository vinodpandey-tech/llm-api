import os

import httpx


async def call_ollama(prompt: str, timeout: float = 5.0):
    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.post(
            os.environ.get("OLLAMA_URL"),
            json={"model": "mistral", "prompt": prompt, "stream": False},
        )
        response.raise_for_status()
        return response.json()
