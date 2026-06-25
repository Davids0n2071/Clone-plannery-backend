import httpx
import os
from app.models.places import PlaceResult

GOOGLE_API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")

# URL base de la API de Google Places (Text Search)
GOOGLE_PLACES_URL = "https://maps.googleapis.com/maps/api/place/textsearch/json"
GOOGLE_PHOTO_URL = "https://maps.googleapis.com/maps/api/place/photo"

async def search_places(query: str, latitude: float, longitude: float) -> list[PlaceResult]:
    """
    Llama a Google Places API y devuelve una lista de lugares.
    'async' significa que no bloquea el servidor mientras espera la respuesta de Google.
    """

    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_PLACES_API_KEY no está configurada en el .env")

    params = {
        "query": query,
        "location": f"{latitude},{longitude}",  # centro de búsqueda
        "radius": 5000,                         # radio en metros (5 km)
        "key": GOOGLE_API_KEY,
        "language": "es"                        # resultados en español
    }

    # httpx.AsyncClient es como abrir un navegador temporal para hacer la petición
    async with httpx.AsyncClient() as client:
        response = await client.get(GOOGLE_PLACES_URL, params=params, timeout=10)

    # Si Google devuelve error HTTP (500, 403, etc.), lanzamos excepción
    response.raise_for_status()

    data = response.json()
    status = data.get("status")

    # Google devuelve su propio campo "status" dentro del JSON
    if status == "REQUEST_DENIED":
        raise ValueError("API Key inválida o sin permisos para Places API")
    if status == "ZERO_RESULTS":
        return []  # no es un error, simplemente no encontró nada
    if status not in ("OK", "ZERO_RESULTS"):
        raise ValueError(f"Google Places API error: {status}")

    results = []
    for place in data.get("results", []):
        # Construir URL de la foto si el lugar tiene fotos
        photo_url = None
        photos = place.get("photos")
        if photos:
            photo_reference = photos[0].get("photo_reference")
            photo_url = (
                f"{GOOGLE_PHOTO_URL}"
                f"?maxwidth=400"
                f"&photo_reference={photo_reference}"
                f"&key={GOOGLE_API_KEY}"
            )

        location = place.get("geometry", {}).get("location", {})

        results.append(PlaceResult(
            name=place.get("name", "Sin nombre"),
            address=place.get("formatted_address", "Sin dirección"),
            latitude=location.get("lat", 0.0),
            longitude=location.get("lng", 0.0),
            rating=place.get("rating"),       # None si no tiene rating
            photo_url=photo_url
        ))

    return results