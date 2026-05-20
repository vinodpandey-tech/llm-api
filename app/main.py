from dotenv import load_dotenv
from fastapi import FastAPI

from app.routes import router

load_dotenv()

app = FastAPI()
app.include_router(router)
