from pydantic import BaseModel
from typing import Optional

# Representa cada plan que el frontend envía al chat
class PlanInfo(BaseModel):
    nombre: str
    direccion: str
    rating: Optional[float] = None

# Lo que el frontend envía al endpoint /chat
class ChatRequest(BaseModel):
    mensaje: str
    userId: str
    planes: list[PlanInfo] = []  # lista vacía si el usuario no tiene planes

# Lo que devolvemos al frontend
class ChatResponse(BaseModel):
    respuesta: str

