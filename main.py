import os
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from astro.calculator import get_planet_positions
from astro.interpreter import interpret
from astro.schemas import ChartRequest
from config import get_config

from datetime import datetime, timezone
from skyfield.api import load, wgs84

from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

# Middleware para agregar charset
class CharsetMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        if isinstance(response, JSONResponse):
            response.headers["Content-Type"] = "application/json; charset=utf-8"
        return response

# Obtener configuración según el entorno
config = get_config()

app = FastAPI(title=config.APP_NAME, debug=config.DEBUG)

app.add_middleware(CharsetMiddleware)

# Configuración de CORS dinámica
# En Render, permitir todos los orígenes temporalmente
cors_origins = ["*"] if "render.com" in os.getenv("RENDER_EXTERNAL_URL", "") else config.CORS_ORIGINS

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=config.ALLOW_CREDENTIALS,
    allow_methods=config.ALLOW_METHODS,
    allow_headers=config.ALLOW_HEADERS,
)

@app.get("/")
async def root():
    return {
        "message": "Astro Reader API",
        "version": "1.0.0",
        "status": "running",
        "environment": "development" if config.DEBUG else "production"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/api/chart/")
async def get_chart(data: ChartRequest, type: str = Query("professional", enum=["professional", "spiritual", "psychological", "youth"])):
    positions = get_planet_positions(
        data.date, str(data.latitude), str(data.longitude)
    )
    reading = interpret(positions, type=type)
    return {
        "positions": positions,
        "reading": reading
    }


