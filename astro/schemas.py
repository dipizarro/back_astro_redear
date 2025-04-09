from pydantic import BaseModel

class ChartRequest(BaseModel):
    date: str
    latitude: float
    longitude: float
