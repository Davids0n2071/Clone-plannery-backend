import httpx
import os
from groq import Groq
from app.models.places import PlaceResult
import json


GOOGLE_API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")

# URL base de la API de Google Places (Text Search)
GOOGLE_PLACES_URL = "https://maps.googleapis.com/maps/api/place/textsearch/json"
GOOGLE_PHOTO_URL = "https://maps.googleapis.com/maps/api/place/photo"

client = Groq()
def generate_descriptions(nombres: list[str]) -> list[str]:
    PROMPT: str ="""You are a Bogotá location description generator. You will receive a list of place names. 
            For each place, generate a concise, engaging description of exactly 20 words or fewer. Return 
            your answer as a JSON array of strings, where each string corresponds to the description of the place 
            at the same index in the input list. Your response must consist solely of this JSON array, with no additional 
            text, explanations, markdown, or code fences and give me your response in spanish."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY no está configurada en el .env")

    # Construye el contexto de planes para incluirlo en el mensaje del usuario
    nombres_texto = "\n".join(nombres)

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": PROMPT
            },
            {
                "role": "user",
                #envia nombres de los lugares para que cree las descripciones
                "content":nombres_texto
            }
        ],
        temperature=0.7,   # 0 = respuestas más exactas, 1 = más creativas
        max_tokens=1024,
    )
    try:
        raw = completion.choices[0].message.content.strip()
        raw = raw.rstrip().rstrip("]").rstrip().rstrip(",") + "]"
        return json.loads(raw)
    except Exception as e:
        print(f"=== ERROR generate_descriptions ===")
        print(f"Respuesta de Groq: {completion.choices[0].message.content}")
        print(f"Error: {str(e)}")
        return [""] * len(nombres)



def get_category(place: dict, query: str) -> str:
    """
    Intenta obtener la categoría del lugar.
    Primero mira los tipos que devuelve Google.
    Si no hay nada útil, usa el query del usuario.
    """
    # tipos que devuelve Google y su traducción legible
    type_map = {
        "restaurant": "Restaurante",
        "food": "Restaurante",
        "cafe": "Café",
        "bar": "Bar",
        "night_club": "Discoteca",
        "museum": "Museo",
        "park": "Parque",
        "shopping_mall": "Centro comercial",
        "store": "Tienda",
        "gym": "Gimnasio",
        "movie_theater": "Cine",
        "tourist_attraction": "Atracción turística",
        "church": "Iglesia",
        "hospital": "Hospital",
        "school": "Colegio",
        "university": "Universidad",
        "lodging": "Hotel",
        "spa": "Spa",
        "amusement_park": "Parque de diversiones",
        "stadium": "Estadio",
    }

    types = place.get("types", [])
    for t in types:
        if t in type_map:
            return type_map[t]

    # si Google no devolvió un tipo reconocido, usa el query
    return query.capitalize()

async def search_places(query: str, latitude: float, longitude: float) -> list[PlaceResult]:
    """
    Llama a Google Places API y devuelve una lista de lugares.
    'async' significa que no bloquea el servidor mientras espera la respuesta de Google.
    """
    import asyncio
    loop = asyncio.get_event_loop()
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_PLACES_API_KEY no está configurada en el .env")

    params = {
        "query": query,
        "location": f"{latitude},{longitude}",  # centro de búsqueda
        "radius": 15000,                         # radio en metros (5 km)
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
    names=[]
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
        names.append(place.get("name", "Sin nombre"))
        location = place.get("geometry", {}).get("location", {})
        results.append(PlaceResult(
            name=place.get("name", "Sin nombre"),
            address=place.get("formatted_address", "Sin dirección"),
            latitude=location.get("lat", 0.0),
            longitude=location.get("lng", 0.0),
            rating=place.get("rating"),       # None si no tiene rating
            photo_url=photo_url,
            category = get_category(place, query)
        ))
    descriptions = await loop.run_in_executor(None, generate_descriptions, names)
    for i, result in enumerate(results):
        result.description = descriptions[i]
    return results