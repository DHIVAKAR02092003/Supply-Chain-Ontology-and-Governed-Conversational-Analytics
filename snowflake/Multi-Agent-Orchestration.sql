-- ============================================================================
-- MULTI-AGENT ORCHESTRATION: ORDER_360_AGENT as Custom Tool
-- ============================================================================
-- This creates a UDF that calls the ORDER_360_AGENT via DATA_AGENT_RUN.
-- The UDF is designed to be added as a GENERIC custom tool to the
-- UNIFIED_PERSONA_AGENT, enabling multi-agent routing for cross-domain queries.
-- ============================================================================

USE ROLE ACCOUNTADMIN;
USE WAREHOUSE COMPUTE_WH;
USE DATABASE SCM_ANALYTICS;
USE SCHEMA CROSS_DOMAIN;


-- ╔══════════════════════════════════════════════════════════════════════════╗
-- ║  STEP 1: CREATE THE STORED PROCEDURE                                     ║
-- ╚══════════════════════════════════════════════════════════════════════════╝

CREATE OR REPLACE PROCEDURE SCM_ANALYTICS.CROSS_DOMAIN.CALL_ORDER_360_AGENT(USER_QUESTION STRING)
RETURNS STRING
LANGUAGE SQL
EXECUTE AS CALLER
AS
BEGIN
  LET sanitized_question STRING := REPLACE(REPLACE(:USER_QUESTION, '\\', '\\\\'), '"', '\\"');
  LET request_json STRING := '{"messages":[{"role":"user","content":[{"type":"text","text":"' || :sanitized_question || '"}]}]}';
  LET result_val STRING := (SELECT SNOWFLAKE.CORTEX.DATA_AGENT_RUN(
    'SCM_ANALYTICS.CROSS_DOMAIN.ORDER_360_AGENT',
    :request_json,
    TRUE
  ));
  RETURN :result_val;
END;


-- ╔══════════════════════════════════════════════════════════════════════════╗
-- ║  STEP 2: VALIDATE THE STORED PROCEDURE                                   ║
-- ╚══════════════════════════════════════════════════════════════════════════╝

-- Test 1: Basic cross-domain question
CALL SCM_ANALYTICS.CROSS_DOMAIN.CALL_ORDER_360_AGENT(
  'What is the total end-to-end lead time from PO to customer delivery?'
);


-- ╔══════════════════════════════════════════════════════════════════════════╗
-- ║  STEP 3: ADD AS CUSTOM TOOL TO UNIFIED_PERSONA_AGENT (Manual via UI)    ║
-- ╚══════════════════════════════════════════════════════════════════════════╝
-- In Snowsight → AI & ML → Agents → UNIFIED_PERSONA_AGENT → Configuration:
--
-- 1. Go to the "Tools" tab
-- 2. Click "Add Tool" → select "Stored Procedure" (Generic)
-- 3. Configure:
--    • Name:        order_360_tool
--    • Description: Calls the Order 360 cross-domain agent for queries
--                   that require data from 2+ supply chain domains
--                   (e.g., end-to-end lead time, procurement-to-delivery
--                   tracking, comparing metrics across Sales + Procurement
--                   + Manufacturing + Logistics).
--    • Procedure:   SCM_ANALYTICS.CROSS_DOMAIN.CALL_ORDER_360_AGENT
--    • Input Schema:
--        {
--          "type": "object",
--          "properties": {
--            "USER_QUESTION": {
--              "type": "string",
--              "description": "The user's cross-domain question to route to the Order 360 agent"
--            }
--          },
--          "required": ["USER_QUESTION"]
--        }
--    • Warehouse: AIML_WH
--
-- 4. Click Save → then Publish


-- ╔══════════════════════════════════════════════════════════════════════════╗
-- ║  STEP 4: ORCHESTRATION ROUTING RULES                                    ║
-- ╚══════════════════════════════════════════════════════════════════════════╝
-- Append this to the Orchestration Instructions in the agent UI:
--
-- ------------------------------------------------------------
-- 10) MULTI-AGENT: ORDER 360 CROSS-DOMAIN ROUTING
-- ------------------------------------------------------------

-- TOOL: order_360_tool
-- PURPOSE: Routes questions to the ORDER_360_AGENT when the question
-- requires data from 2 or more persona domains in a single answer.

-- WHEN TO USE order_360_tool:
-- - User explicitly asks for end-to-end / cross-domain analysis
-- - Question requires joining data across Sales + Procurement,
--   or Manufacturing + Logistics, or any 2+ domains
-- - User asks about total lead time (PO → production → delivery)
-- - User asks to compare metrics across domains (e.g., supplier
--   lead time vs manufacturing cycle time vs transit time)
-- - User asks for order lifecycle tracking (from order placement
--   through procurement, production, shipping, to customer receipt)
-- - User mentions "Order 360", "end-to-end", "full lifecycle",
--   "cross-domain", or "complete order view"

-- WHEN NOT TO USE (use single-domain analyst tools instead):
-- - Question can be answered by a single persona semantic view
-- - User asks about only procurement, only sales, only logistics, etc.
-- - Simple metric queries that don't need cross-domain stitching

-- ROUTING RULES:
-- 1. If the question matches a single domain (Steps A-C in Section 2),
--    use the corresponding analyst tool directly. Do NOT route to Order 360.
-- 2. If the question needs 2+ domains AND matches the Order 360 criteria
--    above, pass the user's question to order_360_tool.
-- 3. When calling order_360_tool, pass the user's original question
--    as-is in the USER_QUESTION parameter. Do not rewrite or summarize it.
-- 4. Present the Order 360 response directly to the user. If the response
--    includes SQL results, format them as a table.
-- 5. Prefix the response with: "Routing to Order 360 (cross-domain)..."

-- EXAMPLES:
-- User: "What is the total lead time from PO to customer delivery?"
--   → order_360_tool (spans Procurement + Manufacturing + Logistics)
-- User: "Compare supplier OTD vs customer OTD"
--   → order_360_tool (spans Procurement + Sales)
-- User: "Track order SO-0001234 from PO through production to shipping"
--   → order_360_tool (full lifecycle)
-- User: "What is the procurement lead time?"
--   → procurement_analyst (single domain, do NOT use Order 360)


-- ╔══════════════════════════════════════════════════════════════════════════╗
-- ║  STEP 5: VALIDATION QUESTIONS FOR MULTI-AGENT ROUTING                   ║
-- ╚══════════════════════════════════════════════════════════════════════════╝

-- After adding the custom tool + routing rules + publishing, test in CoWork:

-- Test A: Should route to Order 360 (cross-domain)
-- "What is the end-to-end lead time from PO to customer delivery?"

-- Test B: Should route to Order 360 (comparing across domains)
-- "Compare supplier on-time delivery rate vs customer on-time delivery rate"

-- Test C: Should route to Order 360 (full lifecycle)
-- "Show me the complete order lifecycle for the most recent sales order"

-- Test D: Should NOT route to Order 360 (single domain → procurement)
-- "What is the average procurement lead time?"

-- Test E: Should NOT route to Order 360 (single domain → sales)
-- "Show me the top 5 customers by order value"

-- Test F: Ambiguous but context-aware (should use sticky context)
-- Ask first: "Show me supplier performance for PowerCell"
-- Then ask: "What about their impact on production delays?"
-- → Second question should route to Order 360 since it spans Procurement + Manufacturing
