# Supply Chain Ontology & Governed Conversational Analytics

> **One Supply Chain. Multiple Personas. One Governed Business Language.**

**Team:** Pro-Scientists | **Leader:** Krishna Apil Chowdary Morampudi | **Size:** 3 | **Hackathon:** CoCo CLI Hackathon GCC Edition

**Live Application:** [https://eqzfdtb-pmktxrp-ceb03210.snowflakecomputing.app](https://eqzfdtb-pmktxrp-ceb03210.snowflakecomputing.app)
**User Name:** KRISHNA
**Password:** Kasmo@123456789

---

## Table of Contents

- [Problem Statement](#problem-statement)
- [Solution Overview](#solution-overview)
- [Architecture](#architecture)
- [Data Architecture (Medallion)](#data-architecture-medallion)
- [Supply Chain Ontology](#supply-chain-ontology)
- [Semantic Views](#semantic-views)
- [Cortex Agent](#cortex-agent)
- [Unstructured Data Processing](#unstructured-data-processing)
- [React Application](#react-application)
- [SPCS Deployment](#spcs-deployment)
- [CoCo Desktop Usage](#coco-desktop-usage)
- [API Endpoints](#api-endpoints)
- [Local Development](#local-development)
- [Project Structure](#project-structure)
- [Environment Variables](#environment-variables)
- [Future Roadmap](#future-roadmap)

---

**Snapshots:**

**1.Home Page:**
<img width="1918" height="1069" alt="image" src="https://github.com/user-attachments/assets/14f1a5de-9dbd-4b6a-be7d-7e21cd9bb319" />

**2. Ontology (Architecture || Live Workflow):**
<img width="1918" height="1078" alt="image" src="https://github.com/user-attachments/assets/4b9ffbd7-afed-48f5-95a3-be84ec93e402" />

**3. Manufacturing Manager (AI Insights) :** 
<img width="1918" height="1066" alt="image" src="https://github.com/user-attachments/assets/e058036a-ebfe-435b-8825-6485fbd120c3" />

**4. Sales Manager (Executive KPI's):**
<img width="1912" height="1009" alt="image" src="https://github.com/user-attachments/assets/4246afc4-8ffc-49c4-8c9a-4ff4a8203d9e" />

**5. Live Agent:** 
<img width="953" height="526" alt="image" src="https://github.com/user-attachments/assets/c3215b83-d3d8-4d0a-9c57-04ac1cce014a" />


## Problem Statement

Supply chain data is scattered across ERP, logistics, supplier, and IoT systems with inconsistent definitions. The same question -- "What is the lead time?" or "What is the cost?" -- yields different answers across teams because each persona interprets the term differently.

**Challenge:** Build an industry ontology expressed as governed semantic views so that a natural language layer returns consistent, trustworthy answers grounded in shared definitions and metrics across all supply chain personas.

---

## Solution Overview

We built an end-to-end governed conversational analytics platform that:

1. **Defines a supply chain ontology** with core entities, relationships, hierarchies, and canonical metrics (OTD, fill rate, days of inventory, landed cost, yield, capacity utilization, forecast accuracy, gross margin)
2. **Encodes the ontology as semantic views** so business meaning -- not raw column names -- drives answers, with explicit disambiguation rules for terms like "lead time", "cost", "delivery date", and "inventory"
3. **Layers governed conversational analytics** via a Cortex Agent so any team asks cross-domain questions and gets one consistent answer
4. **Demonstrates metric consistency** -- the same metric resolves identically across Planning, Procurement, Logistics, Manufacturing, Sales, Warehouse, Quality, and Finance personas
5. **Deploys a production React application** on Snowpark Container Services with persona-based KPI dashboards, live ontology viewer, AI-powered insights, sentiment analysis, and direct agent chat

---

## Architecture

```
+-----------------------------------------------------------------------------------+
|                           REACT JS APPLICATION (SPCS)                             |
|  KPI Dashboards | Ontology Viewer | AI Insights | Sentiment | Agent Chat         |
+-----------------------------------------------------------------------------------+
           |                                          |
           | REST API                                 | Cortex Agent API
           v                                          v
+---------------------+              +------------------------------------------+
|   FastAPI Backend    |              |         CORTEX AGENT                     |
|   - Persona routes   |              |  7 Analyst Tools (Semantic Views)        |
|   - Ontology routes  |              |  Cortex Search (Documents)               |
|   - AI routes        |              |  Custom Tools (Email, ORDER_360)         |
|   - Cache layer      |              |  Code Execution                          |
+---------------------+              |  MCP: GitHub (Skills) + Jira (Tickets)   |
           |                          |  Skills: KPI Health + Ontology Validator  |
           |                          +------------------------------------------+
           |                                          |
           v                                          v
+-----------------------------------------------------------------------------------+
|                           SNOWFLAKE DATA PLATFORM                                 |
|                                                                                   |
|  +------------------+    +-------------------+    +----------------------------+  |
|  | SCM_RAW.RAW_SCH  |    | SCM_RAW.CLEAN     |    | SCM_ANALYTICS              |  |
|  | 40 SAP Tables    |--->| 40 Clean Tables   |--->| .PERSONA (8 Views)         |  |
|  | (Bronze Layer)   |    | (Silver Layer)    |    | .CROSS_DOMAIN (5 Views)    |  |
|  +------------------+    +-------------------+    | .INTERNAL (Base Tables)    |  |
|                                                   | .DOCUMENTS_SCH (Search)    |  |
|                                                   | 9 Semantic Views           |  |
|                                                   +----------------------------+  |
+-----------------------------------------------------------------------------------+
```

---

## Data Architecture (Medallion)

### Bronze Layer -- `SCM_RAW.RAW_SCH` (40 SAP Tables)

Synthetic dataset generated using CoCo Desktop, modeled after the real SAP data dictionary with SAP transaction codes and column naming conventions:

| Category | SAP Tables | Count |
|----------|-----------|-------|
| Sales & Distribution | VBAK, VBAP, VBEP, LIKP, LIPS, KNA1, VTTK, VTTP | 8 |
| Materials Management | MARA, MARC, MARD, MARD_SNAPSHOT, MAST, STPO, MKPF, MSEG, MSKA | 9 |
| Procurement | EKKO, EKPO, EKBE, EBAN | 4 |
| Production | AUFK, AFKO, AFPO, AFRU, RESB, PLAF | 6 |
| Quality | QMEL, QMFE | 2 |
| Finance & Controlling | BKPF, BSEG, COEP, T001 | 4 |
| Master Data | LFA1, T001W, S031, PBIM | 4 |
| Change Management | CDHDR, CDPOS, JEST | 3 |

### Silver Layer -- `SCM_RAW.CLEAN` (40 Transformed Tables)

SAP codes and abbreviations transformed into human-readable, business-friendly column names:

| Clean Table | Source | Description |
|------------|--------|-------------|
| SALES_ORDER_HEADER | VBAK | Customer orders with dates, values |
| SALES_ORDER_ITEM | VBAP | Order line items with materials, quantities |
| PURCHASE_ORDER_HEADER | EKKO | Procurement POs with vendor, dates |
| PURCHASE_ORDER_ITEM | EKPO | PO line items with pricing |
| PRODUCTION_ORDER_HEADER | AUFK | Manufacturing orders |
| QUALITY_NOTIFICATION | QMEL | Quality inspection records |
| INVENTORY_DAILY_SNAPSHOT | MARD_SNAPSHOT | Daily stock positions |
| CUSTOMER_MASTER | KNA1 | Customer reference data |
| VENDOR_MASTER | LFA1 | Supplier reference data |
| MATERIAL_MASTER | MARA | Product catalog |
| ... | ... | *40 tables total* |

### Gold Layer -- `SCM_ANALYTICS` (Analytics Views)

**Persona Views** (`SCM_ANALYTICS.PERSONA`):

| View | Domain | Key Metrics |
|------|--------|-------------|
| PROCUREMENT_PERSONA | Supplier management | PO lead time, supplier OTD, 3-way match, rejection rate |
| MANUFACTURING_PERSONA | Production | Cycle time, first pass yield, scrap/rework, cost per unit |
| WAREHOUSE_PERSONA | Inventory | Stock health, ATP, storage utilization, inventory turns |
| SALES_PERSONA | Customer orders | Order value, fill rate, on-time delivery, lead time |
| LOGISTICS_PERSONA | Shipments | Transit time, carrier performance, delivery performance |
| PLANNING_PERSONA | Demand/capacity | Forecast accuracy, capacity utilization, days of inventory |
| QUALITY_PERSONA | Inspections | Incoming reject rate, final test yield, defect analysis |
| FINANCE_PERSONA | Profitability | Landed cost, gross margin, invoice matching, inventory value |

**Cross-Domain Views** (`SCM_ANALYTICS.CROSS_DOMAIN`):

| View | Purpose |
|------|---------|
| ORDER_360 | End-to-end order lifecycle stitching all personas |
| ORDER_LIFECYCLE_TRACE | Milestone tracking with status across domains |
| SUPPLIER_SCORECARD | Composite supplier scoring (OTD, quality, price) |
| INVENTORY_TURNS | Cross-domain inventory turnover calculation |
| AMBIGUITY_CASE_MAP | Ontology disambiguation reference (8 ambiguous terms) |

---

## Supply Chain Ontology

### Core Entities & Relationships

```
Supplier --> Component --> Procurement --> Quality (Incoming) --> Planning -->
Manufacturing --> Quality (Final Test) --> Warehouse --> Sales --> Logistics --> Customer
```

**Finance** operates across all stages, monitoring costs and profitability.

### Canonical Metrics

| Metric | Definition | Used By |
|--------|-----------|---------|
| On-Time Delivery | % delivered on/before committed date | Procurement, Sales, Logistics |
| Fill Rate | % of ordered quantity fulfilled | Sales, Warehouse |
| Days of Inventory | Days stock covers expected demand | Planning, Warehouse, Finance |
| Landed Cost | Total acquisition + delivery cost (materials + labor + freight + duty) | Finance, Procurement |
| First Pass Yield | % passing quality on first attempt | Manufacturing, Quality |
| Capacity Utilization | % of available capacity in use | Planning, Manufacturing |
| Forecast Accuracy | Forecast vs actual demand match | Planning |
| Gross Margin | (Revenue - Landed Cost) / Revenue | Finance, Sales |

### Ontology Disambiguation Rules

The same business term means different things across personas. The ontology explicitly resolves these:

| Term | Procurement | Manufacturing | Sales | Logistics | Finance |
|------|------------|---------------|-------|-----------|---------|
| **Lead Time** | PO-to-receipt (6d) | Assembly cycle (2d) | Order-to-delivery (12d) | Dispatch-to-doorstep (2d) | N/A |
| **Cost** | PO unit price ($400) | Materials+labor ($450) | Selling price | N/A | Full landed ($480) |
| **Delivery Date** | Supplier-to-warehouse | N/A | Customer received | Customer received | N/A |
| **Inventory** | N/A | N/A | ATP (promise qty) | N/A | Book value ($) |
| **Rejection Rate** | Incoming supplier defects | Final test defects | N/A | N/A | N/A |
| **Fill Rate** | N/A | N/A | Shipped/ordered % | N/A | N/A |
| **Cycle Time** | PO-to-GR days | Assembly days | Order-to-ship days | N/A | N/A |
| **Status** | N/A | N/A | Sales status | Logistics status | Finance status |

These rules are encoded in:
- The `AMBIGUITY_CASE_MAP` cross-domain view
- Each semantic view's `comment` field (custom instructions and guardrails)
- The Cortex Agent's orchestration and routing rules

---

## Semantic Views

9 governed semantic views encode the ontology for Cortex Analyst:

| Semantic View | Schema | Domain | Key Disambiguation |
|--------------|--------|--------|-------------------|
| SV_PROCUREMENT_PERSONA | PERSONA | Procurement | Lead time = PO-to-receipt. Cost = PO price only |
| SV_MANUFACTURING_PERSONA | PERSONA | Manufacturing | Lead time = cycle time. Cost = materials + labor |
| SV_WAREHOUSE_PERSONA | PERSONA | Warehouse | Inventory = full physical breakdown |
| SV_SALES_PERSONA | PERSONA | Sales | Lead time = order-to-delivery. Value = revenue |
| SV_LOGISTICS_PERSONA | PERSONA | Logistics | Lead time = transit time. No cost scope |
| SV_PLANNING_PERSONA | PERSONA | Planning | Demand = forecast vs actual. No cost scope |
| SV_QUALITY_PERSONA | PERSONA | Quality | Rejection = both incoming + final test |
| SV_FINANCE_PERSONA | PERSONA | Finance | Cost = full landed. Margin = profit lens |
| SV_ORDER_360 | CROSS_DOMAIN | Cross-domain | End-to-end order lifecycle with all milestones |

Each semantic view includes:
- Metrics, dimensions, facts, and relationships
- Custom instructions with disambiguation rules
- Guardrails to prevent cross-domain confusion
- Verified queries for accuracy validation

---

## Cortex Agent

### Agent Configuration

| Component | Details |
|-----------|---------|
| Display Name | Supply Chain Ontology Agent |
| Description | Governed conversational analytics across 8 supply chain personas |
| Example Questions | Cross-domain and persona-specific queries |
| Orchestration | Routing rules + guardrails for cross-persona interception |
| Response Instructions | Governed response formatting |

### Tools

| # | Tool Type | Tool Name | Purpose |
|---|----------|-----------|---------|
| 1 | Code Execution | Enabled | Python code execution for complex analytics |
| 2 | Cortex Analyst | FINANCE_ANALYST | Finance domain queries via SV_FINANCE_PERSONA |
| 3 | Cortex Analyst | LOGISTICS_ANALYST | Logistics domain queries via SV_LOGISTICS_PERSONA |
| 4 | Cortex Analyst | MANUFACTURING_ANALYST | Manufacturing domain queries via SV_MANUFACTURING_PERSONA |
| 5 | Cortex Analyst | PROCUREMENT_ANALYST | Procurement domain queries via SV_PROCUREMENT_PERSONA |
| 6 | Cortex Analyst | QUALITY_ANALYST | Quality domain queries via SV_QUALITY_PERSONA |
| 7 | Cortex Analyst | SALES_ANALYST | Sales domain queries via SV_SALES_PERSONA |
| 8 | Cortex Analyst | WAREHOUSE_ANALYST | Warehouse domain queries via SV_WAREHOUSE_PERSONA |
| 9 | Cortex Search | DOCUMENT_SEARCH | Policy, audit, and risk document retrieval |
| 10 | Custom Tool | SEND_EMAIL_TOOL | Send alerts and reports via email |
| 11 | Custom Tool | ORDER_360_TOOL | Multi-agent orchestration -- calls ORDER_360_AGENT for end-to-end order details |

### Skills

| Skill | Trigger | Description |
|-------|---------|-------------|
| scm-kpi-health-check | KPI health queries | Runs canonical KPI queries across all persona views, flags anomalies against industry thresholds, produces red/yellow/green health report |
| scm-ontology-validator | "validate semantic view", "audit SV_*" | Validates semantic views against ontology disambiguation rules, checks cross-domain relationships and metric definitions |

### MCP Integrations

| MCP Server | Type | Purpose |
|-----------|------|---------|
| **GitHub** | Read | Hosts 5 reusable report generation skills (e.g., "Generate a Monthly Business Review report"). Publicly available for other teams. Repo: [GitHub](https://github.com/DHIVAKAR02092003/Supply-Chain-Ontology-and-Governed-Conversational-Analytics) |
| **Jira (Atlassian)** | Write | Raises support tickets for operations teams. Examples: supplier corrective action tickets, low stock replenishment tickets |

### Guardrails & Routing

- Strict routing rules redirect each question to the correct persona tool
- Cross-persona interceptions are handled with disambiguation context
- Out-of-bound questions are rejected with governed responses
- Agent follows ontology disambiguation rules for ambiguous terms

---

## Unstructured Data Processing

### Document Pipeline

1. **Source Documents** (5 PDFs): Contracts, audit reports, production deviation reports, security incident reports, supplier quality assessments
2. **Processing**: Automated pipeline using `AI_PARSE_DOCUMENT` for text extraction
3. **Chunking**: Documents split into retrievable chunks with metadata (file path, size, page index)
4. **Search Service**: `DOCUMENT_SEARCH` Cortex Search Service on `SCM_ANALYTICS.DOCUMENTS_SCH` with `snowflake-arctic-embed-m-v1.5` embeddings
5. **Integration**: Agent queries document search for policy, compliance, and audit questions

---

## React Application

Full-stack application deployed on SPCS:

### Features

| Feature | Description | Technology |
|---------|-------------|------------|
| Persona KPI Dashboards | 8 persona tabs with real-time KPIs, charts, and insights | React + Recharts |
| Live Ontology Viewer | Interactive supply chain flow visualization | Custom React components |
| AI-Powered Key Insights | Dynamic insights generated per persona | Snowflake `AI_COMPLETE` |
| Sentiment Analysis | Feedback sentiment scoring | Snowflake `AI_SENTIMENT` |
| AI Classification | Automated data categorization | Snowflake `AI_CLASSIFY` |
| Speak with Data | Natural language agent chat directly in the app | Cortex Agent API |
| Dark/Light Theme | Toggle between visual themes | CSS + React state |

### Technology Stack

- **Frontend:** React 18, Vite 5, Recharts 2.12, Lucide React, React Router 6
- **Backend:** FastAPI (Python), Snowflake Python Connector
- **Deployment:** Docker (multi-container), Nginx reverse proxy, SPCS

---

## SPCS Deployment

```
+-------------------------------------------+
|         SPCS Compute Pool                  |
|                                            |
|  +---------------+    +-----------------+  |
|  |   Frontend    |    |    Backend      |  |
|  |   (Nginx)     |--->|   (FastAPI)     |  |
|  |   Port: 80    |    |   Port: 8000    |  |
|  +---------------+    +--------+--------+  |
|                                |            |
+--------------------------------|------------+
                                 |
                                 v
                        +-----------------+
                        |   Snowflake     |
                        | SCM_ANALYTICS   |
                        +-----------------+
```

**Deployment Steps:**
1. Build Docker images for frontend (Nginx) and backend (FastAPI)
2. Push to Snowflake Image Repository (`SCM_ANALYTICS.PERSONA.SCM_IMAGES`)
3. Create Compute Pool and Service via `snowflake/spcs_setup.sql`
4. Service endpoint: `https://eqzfdtb-pmktxrp-ceb03210.snowflakecomputing.app`

---

## CoCo Desktop Usage

CoCo Desktop was used across the full solution lifecycle:

| Phase | CoCo Usage |
|-------|-----------|
| **Planning** | Explored SAP data dictionary, designed ontology model, drafted data architecture, outlined persona views |
| **Synthetic Data** | Generated 40 referentially consistent SAP tables with realistic codes, quantities, dates, and relationships |
| **Data Pipeline** | Built Bronze-to-Silver transformations, Silver-to-Gold persona views, cross-domain analytical views |
| **Semantic Views** | Authored 9 semantic views with metrics, dimensions, facts, relationships, custom instructions, and guardrails |
| **Agent Creation** | Configured Cortex Agent with 11 tools, 2 skills, 2 MCP servers, routing rules, and guardrails |
| **Document Pipeline** | Built automated PDF processing pipeline (parse, chunk, search service) |
| **Application** | Scaffolded React + FastAPI application, built components, integrated agent chat |
| **Deployment** | Created Dockerfiles, SPCS compute pool, image repository, and service deployment |
| **Testing** | Validated semantic view accuracy, tested agent responses, verified cross-persona metric consistency |
| **Skills** | Created and published reusable skills (KPI Health Check, Ontology Validator, Metric Resolver, Report Generator, Data Quality Auditor) |

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/personas` | List all 8 personas with metadata |
| GET | `/api/personas/{id}/dashboard` | Full dashboard data (KPIs, charts, insights, ontology) |
| GET | `/api/ontology` | Complete ontology (entities, relationships) |
| GET | `/api/ontology/persona/{id}` | Persona-specific ontology relationships |
| POST | `/api/ai/insights` | AI-generated insights for a persona |
| POST | `/api/ai/sentiment` | Sentiment analysis on feedback data |
| POST | `/api/ai/classify` | AI classification of data |
| POST | `/api/ai/agent` | Cortex Agent conversational endpoint |

---

## Local Development

### Prerequisites

- Python 3.11+
- Node.js 18+
- Snowflake account with `SCM_ANALYTICS` database access

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your Snowflake credentials
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
# Runs on http://localhost:5173, proxies /api/* to port 8000
```

### Docker

```bash
docker-compose up --build
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
```

---

## Project Structure

```
GCC CLI - HACKATHON/
|-- frontend/                  # React application (Vite + Recharts)
|   |-- src/
|   |   |-- api/               # REST API client
|   |   |-- components/        # UI components (ai, charts, kpi, ontology, persona)
|   |   |-- hooks/             # Custom React hooks
|   |   |-- pages/             # Home + PersonaDashboard pages
|   |   +-- main.jsx
|   |-- Dockerfile             # Nginx-based production container
|   +-- nginx.conf
|-- backend/                   # FastAPI application
|   |-- app/
|   |   |-- api/routes/        # REST endpoints (health, personas, ontology, ai)
|   |   |-- services/          # Business logic (snowflake, persona, ontology, ai, agent)
|   |   |-- core/              # Config, cache, persona mapping
|   |   +-- main.py
|   |-- requirements.txt
|   +-- Dockerfile
|-- snowflake/                 # SQL artifacts
|   |-- ontology.sql           # Ontology tables + canonical metrics
|   +-- spcs_setup.sql         # SPCS deployment script
|-- architecture/              # Architecture documentation
|-- documents/                 # Unstructured data (5 PDFs)
|   +-- files/                 # Contract, audit, deviation, security, quality reports
|-- docker-compose.yml         # Multi-container orchestration
|-- .env.example               # Environment variable template
+-- README.md
```

---

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SNOWFLAKE_ACCOUNT` | Snowflake account locator | -- |
| `SNOWFLAKE_USER` | Username | -- |
| `SNOWFLAKE_PASSWORD` | Password | -- |
| `SNOWFLAKE_ROLE` | Role to use | `ACCOUNTADMIN` |
| `SNOWFLAKE_WAREHOUSE` | Warehouse | `COMPUTE_WH` |
| `SNOWFLAKE_DATABASE` | Database | `SCM_ANALYTICS` |
| `SNOWFLAKE_SCHEMA` | Schema | `PERSONA` |
| `CORS_ORIGINS` | Allowed origins | `http://localhost:3000,http://localhost:5173` |
| `CACHE_TTL` | Cache TTL in seconds | `300` |

---

## Future Roadmap

- **Role-Based Access Control (RBAC):** Restrict persona views by Snowflake roles so each team only sees their domain
- **Data Masking:** Apply dynamic data masking policies for sensitive fields (cost, margin, supplier pricing)
- **Real-Time Pipelines:** Add Snowpipe Streaming for near real-time inventory and shipment updates
- **Additional MCP Integrations:** Connect Slack for agent notifications and Google Drive for document ingestion
- **Multi-Language Support:** Extend agent to support queries in multiple languages
- **Evaluation Framework:** Automated agent accuracy testing with verified query benchmarks

---

## Team

| Role | Name |
|------|------|
| Team Leader | Krishna Apil Chowdary Morampudi |
| Team Size | 3 |
| Team Name | Pro-Scientists |

---


