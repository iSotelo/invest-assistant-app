from fastapi import FastAPI

from app.routers import health

app = FastAPI(title="Asistente INVEST - API")

app.include_router(health.router)
