from app.core.persona_config import ONTOLOGY_CONFIG


def get_ontology():
    return ONTOLOGY_CONFIG


def get_persona_relationships(persona_id: str) -> dict | None:
    from app.core.persona_config import PERSONA_CONFIG
    config = PERSONA_CONFIG.get(persona_id)
    if not config:
        return None
    return {
        "persona_id": persona_id,
        "upstream": config["upstream"],
        "downstream": config["downstream"],
        "cross_impact": config["cross_impact"],
        "entity": config["entity"],
        "connected_entities": ONTOLOGY_CONFIG["personas_to_entities"].get(persona_id, []),
    }
