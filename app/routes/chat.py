from fastapi import APIRouter, HTTPException
from app.models.chat import ChatRequest, ChatResponse
from app.services.chat_service import chat_with_groq
import traceback

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):

    # LOG 1 — muestra exactamente qué llegó del frontend
    print("=== BODY RECIBIDO ===")
    print(f"userId: {request.userId}")
    print(f"mensaje: {request.mensaje}")
    print(f"planes recibidos: {len(request.planes)}")
    for p in request.planes:
        print(f"  - {p.nombre} | {p.direccion} | rating: {p.rating}")
    print("=====================")

    try:
        respuesta = chat_with_groq(
            mensaje=request.mensaje,
            planes=request.planes
        )

        # LOG 2 — confirma que Groq respondió algo
        print(f"=== RESPUESTA GROQ ===\n{respuesta}\n=====================")

        return ChatResponse(respuesta=respuesta)

    except ValueError as e:
        print(f"=== ERROR ValueError ===\n{str(e)}\n=======================")
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        # LOG 3 — muestra el error completo con stack trace
        print(f"=== ERROR GROQ ===")
        print(f"Tipo: {type(e).__name__}")
        print(f"Mensaje: {str(e)}")
        print(f"Stack trace completo:")
        traceback.print_exc()
        print(f"=================")

        # Devuelve el error real en vez del mensaje genérico
        raise HTTPException(
            status_code=500,
            detail={
                "error_tipo": type(e).__name__,
                "error_mensaje": str(e)
            }
        )