from fastapi import APIRouter
from app.services.persona_service import get_all_personas, get_persona_dashboard

router = APIRouter(prefix="/api/personas", tags=["personas"])


@router.get("")
def list_personas():
    return get_all_personas()


@router.get("/{persona_id}/dashboard")
def persona_dashboard(persona_id: str):
    result = get_persona_dashboard(persona_id)
    if result is None:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail=f"Persona '{persona_id}' not found")
    return result
