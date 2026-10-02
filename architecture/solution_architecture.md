# Solution Architecture

## Overview

This application demonstrates **Supply Chain Ontology & Governed Analytics** — a pattern where multiple personas consume analytics from the same governed business model while seeing data relevant to their specific role.

## Design Decisions

### Single API Call per Persona
Each persona dashboard is served by a single `GET /api/personas/{id}/dashboard` endpoint that returns all KPIs, charts, insights, and ontology relationships. This minimizes network round-trips and enables the frontend to render instantly on persona switch (with client-side caching).

### Query Pushdown
All aggregations happen in Snowflake via optimized SQL queries. The backend never fetches raw records and aggregates in Python — it pushes computation to the Snowflake warehouse.

### Server-Side Caching
The backend maintains a TTL-based cache (default 5 minutes) for dashboard responses. This means the first persona load hits Snowflake, but subsequent requests serve cached data until TTL expires.

### Client-Side Caching
The React `usePersonaData` hook maintains an in-memory cache per persona. Once a persona's data is fetched, switching between previously-loaded personas is instantaneous (no network call).

### Governed Metric Layer
The `persona_config.py` file serves as the governed configuration layer. Each persona's KPIs and charts are defined with their exact SQL queries, ensuring metric definitions are centralized and auditable. The ontology relationships are also declared here, making the system self-documenting.

## Data Flow

```
User selects persona
        │
        ▼
React (check client cache)
        │ cache miss
        ▼
FastAPI (check server cache)
        │ cache miss
        ▼
Execute KPI queries (8 scalar queries)
Execute chart queries (4 aggregate queries)
Generate insights from KPI values
        │
        ▼
Cache response (server + client)
        │
        ▼
Render dashboard
```

## Ontology Model

The supply chain ontology defines:
1. **Entities** — business objects (Supplier, Component, Plant, etc.)
2. **Relationships** — how entities connect (SUPPLIES, PURCHASED_BY, DELIVERS_TO)
3. **Personas** — which entities each persona is responsible for
4. **Canonical metrics** — shared definitions used consistently across personas

This ensures that when Procurement says "On-Time Delivery" and Logistics says "On-Time Delivery," they mean the same thing (deliveries before committed date) — just measured at different points in the chain.

## SPCS Deployment Architecture

```
┌─────────────────────────────────────────┐
│           SPCS Compute Pool             │
│                                         │
│  ┌──────────────┐  ┌──────────────┐    │
│  │   Frontend   │  │   Backend    │    │
│  │   (nginx)    │──│  (FastAPI)   │    │
│  │   port: 80   │  │  port: 8000  │    │
│  └──────────────┘  └──────┬───────┘    │
│                            │            │
└────────────────────────────┼────────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │    Snowflake    │
                    │  SCM_ANALYTICS  │
                    │    .PERSONA     │
                    └─────────────────┘
```

The two containers run in a single SPCS service. Nginx serves the React SPA and proxies `/api/` to the FastAPI backend. The backend connects to Snowflake using the Python connector.
