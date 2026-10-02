import logging
import json
from app.services.snowflake_service import snowflake_cursor

logger = logging.getLogger(__name__)

MAX_DISPLAY_ROWS = 10

AGENT_FQN = "SCM_ANALYTICS.PERSONA.UNIFIED_PERSONA_AGENT"
AGENT_DISPLAY_NAME = "Ontology Advisor"


def run_agent(message: str, agent_name: str | None = None, conversation_history: list | None = None) -> dict:
    messages = []
    if conversation_history:
        for msg in conversation_history:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if isinstance(content, str):
                messages.append({"role": role, "content": [{"type": "text", "text": content}]})
            elif isinstance(content, list):
                messages.append({"role": role, "content": content})
    messages.append({"role": "user", "content": [{"type": "text", "text": message}]})

    payload = json.dumps({"messages": messages})
    escaped = payload.replace("'", "''")

    sql = f"""
        SELECT TRY_PARSE_JSON(
            SNOWFLAKE.CORTEX.DATA_AGENT_RUN(
                '{AGENT_FQN}',
                $${payload}$$,
                TRUE
            )
        ) AS response
    """

    try:
        logger.info(f"Calling DATA_AGENT_RUN for {AGENT_DISPLAY_NAME}")
        with snowflake_cursor() as cur:
            cur.execute("ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300")
            cur.execute(sql)
            row = cur.fetchone()
            raw = row[0] if row else None

        if raw is None:
            return _error_result("The agent returned no response.")

        if isinstance(raw, str):
            data = json.loads(raw)
        else:
            data = raw

        return _parse_agent_response(data)

    except Exception as e:
        logger.error(f"DATA_AGENT_RUN failed: {e}")
        return _error_result(f"Agent query failed: {str(e)[:300]}")


def _error_result(msg: str) -> dict:
    return {
        "response": msg,
        "tool_calls": [],
        "table_data": None,
        "suggested_queries": [],
        "agent_name": AGENT_DISPLAY_NAME,
    }


def _parse_agent_response(data: dict) -> dict:
    result = {
        "response": "",
        "tool_calls": [],
        "table_data": None,
        "suggested_queries": [],
        "agent_name": AGENT_DISPLAY_NAME,
    }

    content_items = data.get("content", [])
    text_parts = []

    for item in content_items:
        item_type = item.get("type", "")

        if item_type == "text":
            text_parts.append(item.get("text", ""))

        elif item_type == "tool_use":
            tu = item.get("tool_use", {})
            tool_entry = {
                "name": tu.get("name", "tool"),
                "type": tu.get("type", ""),
                "input": "",
                "output": "",
                "status": "running",
            }
            inp = tu.get("input", {})
            if isinstance(inp, dict):
                if "sql" in inp:
                    tool_entry["input"] = inp["sql"]
                elif "pruning_question" in inp:
                    tool_entry["input"] = inp["pruning_question"]
                    tool_entry["name"] = tu.get("name", "semantic_context")
                else:
                    tool_entry["input"] = json.dumps(inp, indent=2)
            result["tool_calls"].append(tool_entry)

        elif item_type == "tool_result":
            tr = item.get("tool_result", {})
            tool_use_id = tr.get("tool_use_id", "")

            # Match to existing tool_call
            matched = None
            for tc in result["tool_calls"]:
                if not matched and tc["status"] == "running":
                    matched = tc

            for c in tr.get("content", []):
                if c.get("type") == "json":
                    json_data = c.get("json", {})

                    # Extract result_set (SQL query results)
                    if "result_set" in json_data:
                        rs = json_data["result_set"]
                        table_data = _parse_result_set(rs)
                        if table_data and table_data["rows"]:
                            result["table_data"] = table_data
                            if matched:
                                matched["output"] = f"{table_data['total_rows']} rows returned"
                                matched["status"] = "completed"

                    # Extract executed SQL for display
                    if "sql" in json_data and matched and not matched["input"]:
                        matched["input"] = json_data["sql"]

                    if matched and matched["status"] == "running":
                        matched["status"] = tr.get("status", "completed")

        elif item_type == "suggested_queries":
            sq = item.get("suggested_queries", [])
            result["suggested_queries"] = [q.get("query", "") for q in sq if q.get("query")]

    # Combine text parts — only keep meaningful agent text, skip internal narration
    result["response"] = "\n\n".join(t.strip() for t in text_parts if t.strip())

    if not result["response"]:
        result["response"] = "The agent processed your request."

    # Mark any remaining running tool calls as completed
    for tc in result["tool_calls"]:
        if tc["status"] == "running":
            tc["status"] = "completed"

    # Filter out semantic_context tool calls (internal, not useful to user)
    result["tool_calls"] = [
        tc for tc in result["tool_calls"]
        if tc.get("type") != "system_agentic_semantic_context"
    ]

    logger.info(f"Agent response: {len(result['response'])} chars, {len(result['tool_calls'])} tools, table={result['table_data'] is not None}")
    return result


def _parse_result_set(rs: dict) -> dict | None:
    meta = rs.get("resultSetMetaData", {})
    row_types = meta.get("rowType", [])
    raw_rows = rs.get("data", [])

    if not row_types or not raw_rows:
        return None

    columns = [rt["name"] for rt in row_types]

    rows = []
    for raw_row in raw_rows:
        row = {}
        for i, col in enumerate(columns):
            val = raw_row[i] if i < len(raw_row) else None
            if val is None:
                row[col] = "—"
            else:
                try:
                    num = float(val)
                    row[col] = round(num, 2) if num != int(num) else int(num)
                except (ValueError, TypeError):
                    row[col] = val
        rows.append(row)

    total = len(rows)
    return {
        "columns": columns,
        "rows": rows[:MAX_DISPLAY_ROWS],
        "total_rows": total,
        "truncated": total > MAX_DISPLAY_ROWS,
    }


def get_available_agents() -> list[dict]:
    return [
        {"id": "ontology_advisor", "name": AGENT_DISPLAY_NAME},
    ]
