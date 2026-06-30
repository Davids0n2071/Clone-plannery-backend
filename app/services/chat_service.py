import os
from groq import Groq
from app.models.chat import PlanInfo

# El cliente de Groq lee GROQ_API_KEY del entorno automáticamente
client = Groq()

SYSTEM_PROMPT = """You are Plannery, a friendly and enthusiastic travel planning assistant.
Your job is to help the user decide which places to visit, based on their saved plans.
You must ALWAYS respond in Spanish, no matter what language the user writes in.

- If the user has saved places, use THAT list to recommend, compare, or build itineraries.
- If the user has NO saved places, you may use your general knowledge to suggest real destinations, attractions, or activities that fit what the user is asking (e.g., "plan for Madrid", "what to see at the beach", etc.).
- Whenever you suggest places that are not in their saved plans, make that clear and encourage them to save them in Plannery so you can track their preferences.
- NEVER invent false information (prices, hours, etc.), but you can suggest well-known real places.
- If the user asks for a plan and has no saved places, offer a suggested route with famous spots and ask if they would like to save some of them.
"""


def build_plans_context(planes: list[PlanInfo]) -> str:
    """Convierte la lista de planes en texto para incluir en el prompt."""
    if not planes:
        return "El usuario aún no tiene lugares guardados en sus planes."

    lines = ["Estos son los lugares que el usuario tiene guardados en Plannery:\n"]
    for i, plan in enumerate(planes, 1):
        rating_text = f" | Rating: {plan.rating}/5" if plan.rating else ""
        lines.append(f"{i}. {plan.nombre} — {plan.direccion}{rating_text}")

    return "\n".join(lines)


def chat_with_groq(mensaje: str, planes: list[PlanInfo]) -> str:
    """
    Llama a Groq con el mensaje del usuario y el contexto de sus planes.
    Devuelve el texto de respuesta del modelo.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY no está configurada en el .env")

    # Construye el contexto de planes para incluirlo en el mensaje del usuario
    plans_context = build_plans_context(planes)

    completion = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                # Enviamos los planes como contexto junto al mensaje del usuario
                "content": f"{plans_context}\n\nPregunta del usuario: {mensaje}"
            }
        ],
        temperature=0.7,   # 0 = respuestas más exactas, 1 = más creativas
        max_tokens=1024,
    )

    return completion.choices[0].message.content