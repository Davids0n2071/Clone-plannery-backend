from app.services.firebase_service import get_db
from app.models.plans import PlanCreate, PlanResponse

COLLECTION = "plans"  # nombre de la colección en Firestore

def create_plan(plan: PlanCreate) -> PlanResponse:
    """Guarda un plan en Firestore y devuelve el documento creado."""
    db = get_db()

    # Convierte el modelo Pydantic a diccionario para Firestore
    plan_data = plan.model_dump()

    # Firestore genera el ID automáticamente con .add()
    _, doc_ref = db.collection(COLLECTION).add(plan_data)

    return PlanResponse(id=doc_ref.id, **plan_data)


def get_plans_by_user(user_id: str) -> list[PlanResponse]:
    """Devuelve todos los planes de un usuario."""
    db = get_db()

    docs = (
        db.collection(COLLECTION)
        .where("userId", "==", user_id)
        .stream()
    )

    plans = []
    for doc in docs:
        data = doc.to_dict()
        plans.append(PlanResponse(id=doc.id, **data))

    return plans


def delete_plan(plan_id: str) -> bool:
    """Elimina un plan por su ID. Devuelve False si no existe."""
    db = get_db()

    doc_ref = db.collection(COLLECTION).document(plan_id)
    doc = doc_ref.get()

    if not doc.exists:
        return False

    doc_ref.delete()
    return True