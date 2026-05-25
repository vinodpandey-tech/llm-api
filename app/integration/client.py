import json
import os

import httpx

from app.common.constants import DEFAULT_MODEL, DEFAULT_OLLAMA_URL


async def call_ollama(prompt: str, timeout: float = 5.0):
    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.post(
            os.environ.get("OLLAMA_URL", DEFAULT_OLLAMA_URL),
            json={
                "model": os.environ.get("MODEL", DEFAULT_MODEL),
                "prompt": prompt,
                "stream": False,
            },
        )
        response.raise_for_status()
        return response.json()


async def stream_ollama(prompt: str):
    async with httpx.AsyncClient(timeout=None) as client:
        async with client.stream(
            "POST",
            os.environ.get("OLLAMA_URL", DEFAULT_OLLAMA_URL),
            json={
                "model": os.environ.get("MODEL", DEFAULT_MODEL),
                "prompt": prompt,
                "stream": True,
            },
        ) as response:
            async for line in response.aiter_lines():
                if not line:
                    continue

                try:
                    data = json.loads(line)
                    yield data  # raw chunk
                except Exception:
                    continue
