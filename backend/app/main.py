from dotenv import load_dotenv
from fastapi import FastAPI

from app.routers import health, validate

load_dotenv()

app = FastAPI(title="Asistente INVEST - API")

app.include_router(health.router)
app.include_router(validate.router)
