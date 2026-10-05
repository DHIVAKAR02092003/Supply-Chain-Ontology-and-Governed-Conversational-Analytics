-- ============================================================================
-- SEND EMAIL CUSTOM TOOL FOR UNIFIED_PERSONA_AGENT
-- ============================================================================
-- This creates a stored procedure that sends emails via SYSTEM$SEND_EMAIL.
-- Designed to be added as a GENERIC custom tool to the agent, allowing
-- users to trigger email sends directly from CoWork conversations.
-- ============================================================================

USE ROLE ACCOUNTADMIN;
USE WAREHOUSE COMPUTE_WH;
USE DATABASE SCM_ANALYTICS;
USE SCHEMA PERSONA;


-- ╔══════════════════════════════════════════════════════════════════════════╗
-- ║  STEP 1: CREATE THE EMAIL NOTIFICATION INTEGRATION                      ║
-- ╚══════════════════════════════════════════════════════════════════════════╝
-- Required once per account. Enables Snowflake to send emails.

CREATE NOTIFICATION INTEGRATION IF NOT EXISTS SCM_EMAIL_NOTIFICATION
  TYPE = EMAIL
  ENABLED = TRUE;


-- ╔══════════════════════════════════════════════════════════════════════════╗
-- ║  STEP 2: CREATE THE STORED PROCEDURE                                    ║
-- ╚══════════════════════════════════════════════════════════════════════════╝

CREATE OR REPLACE PROCEDURE SCM_ANALYTICS.PERSONA.SEND_EMAIL(
  RECIPIENT_EMAIL STRING,
  EMAIL_SUBJECT STRING,
  EMAIL_BODY STRING
)
RETURNS STRING
LANGUAGE SQL
EXECUTE AS CALLER
AS
BEGIN
  CALL SYSTEM$SEND_EMAIL(
    'SCM_EMAIL_NOTIFICATION',
    :RECIPIENT_EMAIL,
    :EMAIL_SUBJECT,
    :EMAIL_BODY,
    'text/html'
  );
  RETURN 'Email sent successfully to ' || :RECIPIENT_EMAIL || ' with subject: ' || :EMAIL_SUBJECT;
END;


-- ╔══════════════════════════════════════════════════════════════════════════╗
-- ║  STEP 3: VALIDATE                                                       ║
-- ╚══════════════════════════════════════════════════════════════════════════╝

CALL SCM_ANALYTICS.PERSONA.SEND_EMAIL(
  'krishna.morampudi@prolim.ai',
  'SCM Agent Test - Email Integration',
  '<h2>Supply Chain Agent - Email Test</h2><p>This is a test email from the <b>UNIFIED_PERSONA_AGENT</b> email custom tool.</p><p>If you received this, the integration is working correctly.</p><br><p><i>Sent via Snowflake CoWork</i></p>'
);


-- ╔══════════════════════════════════════════════════════════════════════════╗
-- ║  STEP 4: ADD AS CUSTOM TOOL TO UNIFIED_PERSONA_AGENT (Manual via UI)    ║
-- ╚══════════════════════════════════════════════════════════════════════════╝
-- In Snowsight → AI & ML → Agents → UNIFIED_PERSONA_AGENT → Configuration:
--
-- 1. Go to the "Tools" tab
-- 2. Click "Add Tool" → select "Stored Procedure" (Generic)
-- 3. Configure:
--    • Name:        send_email_tool
--    • Description: Sends an email to a specified recipient with a subject
--                   and HTML body. Use when the user asks to email, send,
--                   or share a report, summary, alert, or notification.
--                   Supports HTML formatting for tables and styled content.
--    • Procedure:   SCM_ANALYTICS.PERSONA.SEND_EMAIL
--    • Input Schema:
--        {
--          "type": "object",
--          "properties": {
--            "RECIPIENT_EMAIL": {
--              "type": "string",
--              "description": "Email address of the recipient (must be a verified Snowflake user email)"
--            },
--            "EMAIL_SUBJECT": {
--              "type": "string",
--              "description": "Subject line of the email"
--            },
--            "EMAIL_BODY": {
--              "type": "string",
--              "description": "HTML body content of the email. Use HTML tags for formatting: <h2> for headings, <table> for data tables, <b> for bold, <p> for paragraphs."
--            }
--          },
--          "required": ["RECIPIENT_EMAIL", "EMAIL_SUBJECT", "EMAIL_BODY"]
--        }
--    • Warehouse: AIML_WH
--
-- 4. Click Save → then Publish


-- ╔══════════════════════════════════════════════════════════════════════════╗
-- ║  STEP 5: ORCHESTRATION ROUTING RULES                                     ║
-- ╚══════════════════════════════════════════════════════════════════════════╝
-- Append this to the Orchestration Instructions in the agent UI:

-- ------------------------------------------------------------
-- 11) EMAIL NOTIFICATION TOOL
-- ------------------------------------------------------------

-- TOOL: send_email_tool
-- PURPOSE: Sends email notifications with reports, alerts, or summaries.

-- WHEN TO USE send_email_tool:
-- - User says "email this to...", "send this report to...",
--   "share this with...", "notify...", "mail this to..."
-- - User asks to send a summary, alert, or report via email
-- - After generating a report, user asks to email/share it

-- WHEN NOT TO USE:
-- - User just asks for data or a report without mentioning email
-- - User wants to see results on screen only

-- EMAIL FORMATTING RULES:
-- 1. Always format the email body as HTML for readability.
-- 2. Use <h2> for the report title.
-- 3. Use <table border="1" cellpadding="5"> for data tables with
--    <th> headers and <td> cells.
-- 4. Use <b> for key metrics and <p> for paragraphs.
-- 5. Add a footer: <hr><p><i>Generated by TechNova SCM Agent
--    via Snowflake CoWork</i></p>
-- 6. If the user doesn't specify a recipient, ask for the email
--    address before sending.
-- 7. IMPORTANT: Only verified Snowflake user emails can receive
--    emails. If the send fails, inform the user that the recipient
--    email must belong to a verified Snowflake user in this account.

-- WORKFLOW:
-- Step 1: Generate the report/data using the appropriate analyst tool.
-- Step 2: Format the results as an HTML email body.
-- Step 3: Call send_email_tool with recipient, subject, and HTML body.
-- Step 4: Confirm to the user: "Email sent to [recipient] with
--         subject: [subject]"

-- EXAMPLES:
-- User: "Send the procurement lead time summary to krishna.morampudi@prolim.ai"
--   → First query procurement_analyst for data
--   → Then call send_email_tool with formatted HTML results
-- User: "Email me the top 5 suppliers by OTD"
--   → Query procurement_analyst
--   → Format as HTML table
--   → Send to the user's email (krishna.morampudi@prolim.ai)


-- ╔══════════════════════════════════════════════════════════════════════════╗
-- ║  STEP 6: VALIDATION QUESTIONS FOR EMAIL TOOL IN COWORK                   ║
-- ╚══════════════════════════════════════════════════════════════════════════╝

-- Test A: Direct email send
-- "Send an email to krishna.morampudi@prolim.ai with subject 'Daily SCM Summary'
--  and body 'All systems operational. No alerts today.'"

-- Test B: Report + email (two-step)
-- "What are the top 5 suppliers by on-time delivery rate?
--  Now email this to krishna.morampudi@prolim.ai"

-- Test C: Generate and email in one request
-- "Generate a procurement spend summary and email it to krishna.morampudi@prolim.ai"

-- Test D: Should NOT trigger email (no email intent)
-- "Show me the top 5 customers by order value"
