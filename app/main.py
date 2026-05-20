import dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.routes import router

app = FastAPI()
dotenv.load_dotenv()

# API routes
app.include_router(router)

# Serve UI
app.mount("/ui", StaticFiles(directory="ui"), name="ui")


# Optional: root route → open UI directly
@app.get("/")
async def root():
    return FileResponse("ui/index.html")
