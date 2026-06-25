import httpx
from fastapi import APIRouter, HTTPException
from app.models.places import PlaceSearchRequest, PlaceResult
from app.services.places_service import search_places

router = APIRouter(prefix="/places", tags=["places"])

@router.post("/search", response_model=list[PlaceResult])
async def search_places_endpoint(request: PlaceSearchRequest):
    """
    Recibe query + coordenadas y devuelve lista de lugares de Google.
    """
    try:
        places = await search_places(
            query=request.query,
            latitude=request.latitude,
            longitude=request.longitude
        )
        return places

    except ValueError as e:
        # Error controlado (API Key mala, sin resultados, etc.)
        raise HTTPException(status_code=400, detail=str(e))

    except httpx.TimeoutException:
        # Google tardó demasiado en responder
        raise HTTPException(status_code=504, detail="Google Places API no respondió a tiempo")

    except httpx.HTTPStatusError as e:
        # Google respondió con error HTTP
        raise HTTPException(status_code=502, detail=f"Error de Google Places: {e.response.status_code}")

    except Exception as e:
        # Cualquier otro error inesperado
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")