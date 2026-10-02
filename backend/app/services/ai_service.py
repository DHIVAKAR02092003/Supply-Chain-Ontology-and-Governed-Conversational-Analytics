import logging
import json
from app.services.snowflake_service import execute_query, execute_scalar

logger = logging.getLogger(__name__)

AI_MODEL = "llama3.1-8b"


def generate_ai_insights(persona_id: str, persona_name: str, kpis: list[dict]) -> list[str]:
    kpi_summary = ", ".join(
        f"{k['name']}: {k['value']} {k['unit']}" for k in kpis if k["value"] != "N/A"
    )
    prompt = (
        f"You are a supply chain analyst for the {persona_name} team in a laptop manufacturing company. "
        f"Given these current KPIs: [{kpi_summary}], generate exactly 4 concise business insights. "
        f"Each insight should be one sentence. Focus on cross-domain supply chain impacts and actionable observations. "
        f"Return ONLY a JSON array of 4 strings, no other text."
    )
    try:
        escaped = prompt.replace("'", "''")
        result = execute_scalar(
            f"SELECT AI_COMPLETE('{AI_MODEL}', '{escaped}')"
        )
        if result:
            text = str(result).strip()
            
            # Handle doubly-stringified JSON from Snowflake
            if text.startswith('"') and text.endswith('"'):
                try:
                    parsed_str = json.loads(text)
                    if isinstance(parsed_str, str):
                        text = parsed_str
                except json.JSONDecodeError:
                    pass
                    
            # Strip markdown formatting if present
            if text.startswith("```"):
                lines = text.split("\n")
                if len(lines) >= 3:
                    text = "\n".join(lines[1:-1])
                    if text.strip().startswith("json"):
                        text = text.strip()[4:].strip()
                    
            start = text.find("[")
            end = text.rfind("]") + 1
            if start != -1 and end > start:
                try:
                    insights = json.loads(text[start:end])
                    if isinstance(insights, list) and len(insights) >= 1:
                        return [str(i) for i in insights[:4]]
                except json.JSONDecodeError:
                    pass
        logger.warning("AI_COMPLETE returned unexpected format, falling back")
    except Exception as e:
        logger.warning(f"AI insights generation failed for {persona_id}: {e}")
    return _fallback_insights(persona_id, kpis)


def _fallback_insights(persona_id: str, kpis: list[dict]) -> list[str]:
    kpi_map = {k["id"]: k["value"] for k in kpis}
    if persona_id == "procurement":
        return [
            f"Supplier on-time delivery stands at {kpi_map.get('supplier_otd', 'N/A')}%, directly impacting downstream manufacturing schedules.",
            f"With an average lead time of {kpi_map.get('avg_lead_time', 'N/A')} days, sourcing efficiency remains a critical focus.",
            f"Total PO value of {kpi_map.get('total_po_value', 'N/A')}M USD indicates significant recent procurement activity.",
            f"Supplier rejection rate is {kpi_map.get('supplier_rejection', 'N/A')}%, which may cause quality concerns if left unchecked.",
        ]
    elif persona_id == "manufacturing":
        return [
            f"First pass yield of {kpi_map.get('first_pass_yield', 'N/A')}% indicates the current efficiency of assembly processes.",
            f"Schedule adherence is currently at {kpi_map.get('schedule_adherence', 'N/A')}%.",
            f"Manufacturing has produced {kpi_map.get('total_produced', 'N/A')} units this period.",
            f"Make-to-Order ratio is {kpi_map.get('mto_ratio', 'N/A')}%, highlighting demand-driven production.",
        ]
    return ["All KPIs are being monitored and are within expected operational ranges."]


def chat_with_data(message: str, persona_context: str | None = None) -> str:
    system_ctx = (
        "You are a supply chain analytics agent for a laptop manufacturing company. "
        "You have access to data across these domains: Procurement, Manufacturing, Warehouse, "
        "Sales, Logistics, Quality, and Finance. The supply chain flows from Supplier -> Component -> "
        "Procurement -> Quality Inspection -> Manufacturing -> Final Test -> Warehouse -> Sales -> "
        "Logistics -> Customer. Finance oversees cost controls across all stages. "
        "Answer questions concisely using supply chain terminology. "
        "If you reference metrics, use standard SCM KPIs like OTD, fill rate, yield, landed cost, etc."
    )
    if persona_context:
        system_ctx += f" Current context: {persona_context}"

    prompt_obj = [
        {"role": "system", "content": system_ctx},
        {"role": "user", "content": message},
    ]
    try:
        escaped = json.dumps(prompt_obj).replace("'", "''")
        result = execute_scalar(
            f"SELECT AI_COMPLETE('{AI_MODEL}', PARSE_JSON('{escaped}'), OBJECT_CONSTRUCT('temperature', 0.4))"
        )
        if result:
            try:
                parsed = json.loads(str(result))
                if isinstance(parsed, dict) and "choices" in parsed:
                    return parsed["choices"][0]["messages"]
                if isinstance(parsed, dict) and "messages" in parsed:
                    return parsed["messages"]
            except (json.JSONDecodeError, KeyError, IndexError):
                pass
            return str(result).strip()
    except Exception as e:
        logger.error(f"AI chat failed: {e}")
    return "I'm sorry, I couldn't process your query right now. Please try again."


def get_stock_risk_classifications() -> list[dict]:
    query = """
        SELECT 
            PRODUCT_NAME,
            PHYSICAL_STOCK_QTY,
            STORAGE_UTILIZATION_PCT,
            AVAILABLE_TO_PROMISE_QTY,
            AI_CLASSIFY(
                CONCAT('Product: ', PRODUCT_NAME, 
                       ', Stock qty: ', PHYSICAL_STOCK_QTY::STRING, 
                       ', Utilization: ', STORAGE_UTILIZATION_PCT::STRING, '%',
                       ', Available to promise: ', AVAILABLE_TO_PROMISE_QTY::STRING),
                ['Critical - Reorder Now', 'Low Stock - Monitor', 'Healthy', 'Overstocked']
            ) AS AI_RISK_CLASSIFICATION
        FROM SCM_ANALYTICS.PERSONA.WAREHOUSE_PERSONA
        WHERE SNAPSHOT_DATE = (SELECT MAX(SNAPSHOT_DATE) FROM SCM_ANALYTICS.PERSONA.WAREHOUSE_PERSONA)
          AND PRODUCT_CATEGORY = 'LAPTOP'
        ORDER BY PRODUCT_NAME
    """
    try:
        rows = execute_query(query)
        results = []
        for row in rows:
            classification = row.get("AI_RISK_CLASSIFICATION", "{}")
            if isinstance(classification, str):
                try:
                    classification = json.loads(classification)
                except json.JSONDecodeError:
                    classification = {"labels": [classification]}
            
            risk_label = "Unknown"
            if isinstance(classification, dict) and "labels" in classification and classification["labels"]:
                risk_label = classification["labels"][0]
            elif isinstance(classification, str):
                risk_label = classification

            results.append({
                "product": row["PRODUCT_NAME"],
                "stock_qty": row["PHYSICAL_STOCK_QTY"],
                "utilization_pct": row["STORAGE_UTILIZATION_PCT"],
                "atp": row["AVAILABLE_TO_PROMISE_QTY"],
                "risk_label": risk_label,
            })
        return results
    except Exception as e:
        logger.error(f"Stock risk classification failed: {e}")
        return []


def get_quality_sentiment() -> list[dict]:
    query = """
        SELECT 
            NOTIFICATION_NUMBER,
            MATERIAL_NAME,
            SUPPLIER_NAME,
            INSPECTION_TYPE,
            REJECTED_QTY,
            REJECTION_RATE_PCT,
            AI_SENTIMENT(
                CONCAT('Quality notification for ', MATERIAL_NAME, 
                       ' from supplier ', COALESCE(SUPPLIER_NAME, 'unknown'),
                       '. Inspection type: ', INSPECTION_TYPE,
                       '. Rejected quantity: ', REJECTED_QTY::STRING,
                       ' units with rejection rate of ', REJECTION_RATE_PCT::STRING, '%.')
            ) AS SENTIMENT_SCORE
        FROM SCM_ANALYTICS.PERSONA.QUALITY_PERSONA
        WHERE INSPECTION_MONTH = (
            SELECT MAX(INSPECTION_MONTH) FROM SCM_ANALYTICS.PERSONA.QUALITY_PERSONA
        )
        ORDER BY REJECTION_RATE_PCT DESC
        LIMIT 15
    """
    try:
        rows = execute_query(query)
        results = []
        for row in rows:
            sentiment_data = row.get("SENTIMENT_SCORE", "{}")
            sentiment_score = 0.0
            
            if isinstance(sentiment_data, str):
                try:
                    parsed = json.loads(sentiment_data)
                    if "categories" in parsed and parsed["categories"]:
                        sentiment_str = parsed["categories"][0].get("sentiment", "neutral").lower()
                        if sentiment_str == "positive":
                            sentiment_score = 1.0
                        elif sentiment_str == "negative":
                            sentiment_score = -1.0
                except json.JSONDecodeError:
                    pass
            elif isinstance(sentiment_data, (int, float)):
                 sentiment_score = float(sentiment_data)

            results.append({
                "notification": row["NOTIFICATION_NUMBER"],
                "material": row["MATERIAL_NAME"],
                "supplier": row.get("SUPPLIER_NAME", "N/A"),
                "inspection_type": row["INSPECTION_TYPE"],
                "rejected_qty": row["REJECTED_QTY"],
                "rejection_rate": row["REJECTION_RATE_PCT"],
                "sentiment": sentiment_score,
            })
        return results
    except Exception as e:
        logger.error(f"Quality sentiment analysis failed: {e}")
        return []
