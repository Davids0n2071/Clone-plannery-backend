import os
from groq import Groq
from app.models.chat import PlanInfo

# El cliente de Groq lee GROQ_API_KEY del entorno automáticamente
client = Groq()

SYSTEM_PROMPT = """Eres Plannery, un asistente amable y entusiasta de planificación de viajes y salidas.
Tu trabajo es ayudar al usuario a decidir qué lugares visitar basándote en sus planes guardados.
Siempre respondes en español, de forma clara y concisa.
Si el usuario no tiene planes guardados, anímalo a buscar lugares interesantes.
No inventes lugares que no estén en la lista de planes del usuario."""


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