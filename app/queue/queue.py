import asyncio

# prevents memory explosion under load
request_queue = asyncio.Queue(maxsize=3)
