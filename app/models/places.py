from pydantic import BaseModel
from typing import Optional

# Lo que el frontend nos ENVÍA
class PlaceSearchRequest(BaseModel):
    query: str          # texto de búsqueda, ej: "restaurantes en Bogotá"
    latitude: float     # coordenada del usuario
    longitude: float

# Lo que nosotros le DEVOLVEMOS al frontend (un lugar)
class PlaceResult(BaseModel):
    name: str
    address: str
    latitude: float
    longitude: float
    rating: Optional[float] = None   # Optional = puede venir vacío
    photo_url: Optional[str] = None
    category: Optional[str] = None
    description : Optional[str] = None