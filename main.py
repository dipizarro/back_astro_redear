from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from astro.calculator import get_planet_positions
from astro.interpreter import interpret
from astro.schemas import ChartRequest

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

app = FastAPI()

app.add_middleware(CharsetMiddleware)

# Configuración de CORS para producción
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://tu-frontend.vercel.app",  # Reemplaza con tu dominio de Vercel
        "http://localhost:3000",  # Para desarrollo local
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

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


