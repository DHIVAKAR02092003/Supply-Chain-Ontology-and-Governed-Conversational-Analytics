from fastapi import APIRouter
from app.services.ontology_service import get_ontology, get_persona_relationships

router = APIRouter(prefix="/api/ontology", tags=["ontology"])


@router.get("")
def ontology():
    return get_ontology()


@router.get("/persona/{persona_id}")
def persona_ontology(persona_id: str):
    result = get_persona_relationships(persona_id)
    if result is None:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail=f"Persona '{persona_id}' not found")
    return result
