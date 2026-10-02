from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.ai_service import (
    get_stock_risk_classifications,
    get_quality_sentiment,
    generate_ai_insights,
)
from app.services.agent_service import run_agent, get_available_agents
from app.core.persona_config import PERSONA_CONFIG
from app.services.persona_service import get_persona_dashboard

router = APIRouter(prefix="/api/ai", tags=["ai"])


class ChatRequest(BaseModel):
    message: str
    conversation_history: list | None = None


@router.post("/chat")
def ai_chat(request: ChatRequest):
    result = run_agent(
        message=request.message,
        conversation_history=request.conversation_history,
    )
    return result


@router.get("/agents")
def list_agents():
    return get_available_agents()


@router.get("/insights/{persona_id}")
def ai_insights(persona_id: str):
    config = PERSONA_CONFIG.get(persona_id)
    if not config:
        raise HTTPException(status_code=404, detail=f"Persona '{persona_id}' not found")
    dashboard = get_persona_dashboard(persona_id)
    kpis = dashboard["kpis"] if dashboard else []
    insights = generate_ai_insights(persona_id, config["name"], kpis)
    return {"insights": insights}


@router.get("/stock-risk")
def stock_risk():
    return get_stock_risk_classifications()


@router.get("/quality-sentiment")
def quality_sentiment():
    return get_quality_sentiment()
