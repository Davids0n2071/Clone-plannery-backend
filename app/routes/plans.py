from fastapi import APIRouter, HTTPException
from app.models.plans import PlanCreate, PlanResponse
from app.services.plans_service import create_plan, get_plans_by_user, delete_plan

router = APIRouter(prefix="/plans", tags=["plans"])


@router.post("/", response_model=PlanResponse)
def create_plan_endpoint(plan: PlanCreate):
    try:
        return create_plan(plan)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar el plan: {str(e)}")

def get_plans_endpoint(user_id: str):
    try:
        return get_plans_by_user(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener los planes: {str(e)}")

@router.delete("/{plan_id}")
def delete_plan_endpoint(plan_id: str):
    try:
        deleted = delete_plan(plan_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Plan no encontrado")
        return {"message": "Plan eliminado correctamente"}
    except HTTPException:
        raise  # re-lanza el 404 sin envolverlo
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar el plan: {str(e)}")