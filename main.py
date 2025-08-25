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

# Configuración de CORS - Permitir todos los orígenes temporalmente
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todos los orígenes
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "Astro Reader API",
        "version": "1.0.0",
        "status": "running",
        "environment": "development" if config.DEBUG else "production",
        "cors_enabled": True
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/test")
async def test_endpoint():
    return {"message": "Test endpoint working", "cors": "enabled"}

@app.post("/api/chart/")
async def get_chart(data: ChartRequest, type: str = Query("professional", enum=["professional", "spiritual", "psychological", "youth"])):
    try:
        positions = get_planet_positions(
            data.date, str(data.latitude), str(data.longitude)
        )
        reading = interpret(positions, type=type)
        
        # Estructura que espera el frontend
        return {
            "positions": positions,
            "reading": {
                type: reading  # Anidar bajo el tipo solicitado
            }
        }
    except Exception as e:
        return {
            "error": str(e),
            "type": "chart_error",
            "message": "Error processing chart request"
        }


