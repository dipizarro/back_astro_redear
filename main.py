from fastapi import FastAPI
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

# ⭐️ Aquí ponemos cualquier origen para pruebas (puedes restringir después)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción deberías poner ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/chart/")
async def get_chart(data: ChartRequest):
    positions = get_planet_positions(
        data.date, str(data.latitude), str(data.longitude)
    )
    reading = interpret(positions, data.type)  # <--- pasa el tipo
    return {
        "positions": positions,
        "reading": reading
    }


