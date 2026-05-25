import asyncio
from dataclasses import dataclass

from pydantic import BaseModel


class GenerateRequest(BaseModel):
    prompt: str
    request_id: str


@dataclass
class QueueRequest:
    prompt: str
    response_queue: asyncio.Queue  # token stream channel
    request_id: str
