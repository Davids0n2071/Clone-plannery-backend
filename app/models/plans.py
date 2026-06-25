from pydantic import BaseModel
from typing import Optional

# Lo que el frontend envía para crear un plan
class PlanCreate(BaseModel):
    userId: str
    name: str
    address: str
    latitude: float
    longitude: float
    rating: Optional[float] = None
    photo_url: Optional[str] = None

# Lo que devolvemos al frontend (incluye el id generado por Firestore)
class PlanResponse(BaseModel):
    id: str
    userId: str
    name: str
    address: str
    latitude: float
    longitude: float
    rating: Optional[float] = None
    photo_url: Optional[str] = None