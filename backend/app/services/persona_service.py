import logging
import concurrent.futures
from app.core.persona_config import PERSONA_CONFIG
from app.core.cache import cache
from app.services.snowflake_service import execute_query, execute_scalar

logger = logging.getLogger(__name__)


def get_all_personas() -> list[dict]:
    return [
        {
            "id": p["id"],
            "name": p["name"],
            "icon": p["icon"],
            "description": p["description"],
            "entity": p["entity"],
        }
        for p in PERSONA_CONFIG.values()
    ]


def get_persona_dashboard(persona_id: str) -> dict | None:
    config = PERSONA_CONFIG.get(persona_id)
    if not config:
        return None

    cache_key = f"dashboard_{persona_id}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        kpis_future = executor.submit(_fetch_kpis, config)
        charts_future = executor.submit(_fetch_charts, config)
        
        kpis = kpis_future.result()
        charts = charts_future.result()
        
    insights = _generate_insights(persona_id, kpis)

    dashboard = {
        "persona": {
            "id": config["id"],
            "name": config["name"],
            "icon": config["icon"],
            "description": config["description"],
            "entity": config["entity"],
            "why_matters": config["why_matters"],
        },
        "ontology": {
            "upstream": config["upstream"],
            "downstream": config["downstream"],
            "cross_impact": config["cross_impact"],
        },
        "kpis": kpis,
        "charts": charts,
        "insights": insights,
    }

    cache.set(cache_key, dashboard)
    return dashboard


def _fetch_kpis(config: dict) -> list[dict]:
    def fetch_single(kpi_def):
        try:
            value = execute_scalar(kpi_def["query"])
            return {
                "id": kpi_def["id"],
                "name": kpi_def["name"],
                "value": _format_value(value),
                "unit": kpi_def["unit"],
                "description": kpi_def["description"],
            }
        except Exception as e:
            logger.warning(f"KPI query failed for {kpi_def['id']}: {e}")
            return {
                "id": kpi_def["id"],
                "name": kpi_def["name"],
                "value": "N/A",
                "unit": kpi_def["unit"],
                "description": kpi_def["description"],
            }

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        kpis = list(executor.map(fetch_single, config["kpis"]))
    return kpis


def _fetch_charts(config: dict) -> list[dict]:
    def fetch_single(chart_def):
        try:
            data = execute_query(chart_def["query"])
            return {
                "id": chart_def["id"],
                "title": chart_def["title"],
                "type": chart_def["type"],
                "data": data,
            }
        except Exception as e:
            logger.warning(f"Chart query failed for {chart_def['id']}: {e}")
            return {
                "id": chart_def["id"],
                "title": chart_def["title"],
                "type": chart_def["type"],
                "data": [],
            }

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        charts = list(executor.map(fetch_single, config["charts"]))
    return charts


def _generate_insights(persona_id: str, kpis: list[dict]) -> list[str]:
    insights = []
    kpi_map = {k["id"]: k["value"] for k in kpis}

    if persona_id == "procurement":
        insights.append(f"Supplier on-time delivery stands at {kpi_map.get('supplier_otd', 'N/A')}%, directly impacting downstream manufacturing schedules.")
        insights.append(f"With an average lead time of {kpi_map.get('avg_lead_time', 'N/A')} days, sourcing efficiency remains a critical focus.")
        insights.append(f"Total PO value of {kpi_map.get('total_po_value', 'N/A')}M USD indicates significant recent procurement activity.")
        insights.append(f"Supplier rejection rate is {kpi_map.get('supplier_rejection', 'N/A')}%, which may cause quality concerns if left unchecked.")
    elif persona_id == "manufacturing":
        insights.append(f"First pass yield of {kpi_map.get('first_pass_yield', 'N/A')}% indicates the current efficiency of assembly processes.")
        insights.append(f"Schedule adherence is currently at {kpi_map.get('schedule_adherence', 'N/A')}%. Any deviations could cause delays in warehouse replenishment.")
        insights.append(f"Manufacturing operations have successfully produced {kpi_map.get('total_produced', 'N/A')} units this period.")
        insights.append(f"Make-to-Order ratio is {kpi_map.get('mto_ratio', 'N/A')}%, highlighting the demand-driven nature of current production batches.")
    elif persona_id == "warehouse":
        insights.append(f"Total inventory value is {kpi_map.get('total_inventory_value', 'N/A')}M USD, utilizing {kpi_map.get('avg_utilization', 'N/A')}% of available warehouse storage space.")
        insights.append(f"Currently {kpi_map.get('healthy_stock_pct', 'N/A')}% of SKUs maintain healthy stock levels, ensuring smooth fulfillment.")
        insights.append(f"There are {kpi_map.get('out_of_stock', 'N/A')} products out of stock, which may pose an immediate risk to backorder levels.")
        insights.append(f"Effective inventory management here acts as the vital buffer between production volatility and customer demand.")
    elif persona_id == "sales":
        insights.append(f"Total revenue has reached {kpi_map.get('total_revenue', 'N/A')}M USD across all active sales orders.")
        insights.append(f"Customer on-time delivery is performing at {kpi_map.get('on_time_delivery', 'N/A')}%, heavily reliant on upstream logistics and warehouse efficiency.")
        insights.append(f"The current order fill rate is {kpi_map.get('fill_rate', 'N/A')}%, indicating how completely customer requests are being met.")
        bo = kpi_map.get('backorder_count', 'N/A')
        if bo != 'N/A' and str(bo) != '0':
            insights.append(f"With {bo} items backordered, there is a clear signal for manufacturing and procurement to align supply.")
        else:
            insights.append("No items are currently backordered, showing excellent alignment between supply and demand.")
    elif persona_id == "logistics":
        insights.append(f"Logistics on-time rate is {kpi_map.get('otd_rate', 'N/A')}%, reflecting the final delivery experience for customers.")
        insights.append(f"Average transit time is {kpi_map.get('avg_transit_time', 'N/A')} days across all active carriers.")
        insights.append(f"Dispatched {kpi_map.get('total_shipments', 'N/A')} total shipments, serving as the critical last-mile link in the supply chain.")
        insights.append(f"A total of {kpi_map.get('late_shipments', 'N/A')} shipments were delivered late, which may necessitate carrier performance reviews.")
    elif persona_id == "quality":
        insights.append(f"Incoming material rejection rate is {kpi_map.get('incoming_rejection', 'N/A')}%, acting as the first gatekeeper against supplier defects.")
        insights.append(f"Final test rejection rate is {kpi_map.get('final_test_rejection', 'N/A')}%, indicating the overall stability of the manufacturing process.")
        insights.append(f"A total of {kpi_map.get('total_rejected_qty', 'N/A')} units were rejected, representing potential waste and rework costs.")
        insights.append(f"There are {kpi_map.get('qc_hold_impact', 'N/A')} units currently on QC hold, temporarily blocking them from warehouse availability.")
    elif persona_id == "finance":
        insights.append(f"Average gross margin sits at {kpi_map.get('gross_margin', 'N/A')}%, summarizing the overall profitability of the supply network.")
        insights.append(f"Total landed cost is {kpi_map.get('total_landed_cost', 'N/A')}M USD, heavily influenced by upstream procurement and manufacturing efficiencies.")
        insights.append(f"Freight costs represent {kpi_map.get('freight_pct', 'N/A')}% of landed cost, highlighting the financial impact of logistics operations.")
        insights.append(f"Inventory achieves {kpi_map.get('avg_turns', 'N/A')}x annualized turns, impacting working capital liquidity and storage overhead.")

    if not insights:
        insights.append("All KPIs are being monitored and are within expected operational ranges.")
    return insights


def _format_value(value) -> str:
    if value is None:
        return "N/A"
    if isinstance(value, float):
        if value == int(value):
            return str(int(value))
        return str(round(value, 1))
    return str(value)
