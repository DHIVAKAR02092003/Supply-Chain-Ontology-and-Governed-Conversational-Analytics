PERSONA_CONFIG = {
    "procurement": {
        "id": "procurement",
        "name": "Procurement Manager",
        "view": "PROCUREMENT_PERSONA",
        "icon": "ShoppingCart",
        "description": "Sourcing laptop components from reliable suppliers at optimal cost and lead time.",
        "entity": "Purchase Order",
        "why_matters": "Controls the inflow of raw materials and components. Procurement decisions on supplier selection, pricing, and delivery terms directly impact manufacturing schedules, product cost, and ultimately customer satisfaction.",
        "upstream": ["Supplier", "Component"],
        "downstream": ["Manufacturing", "Quality", "Finance"],
        "cross_impact": "A supplier delay in procurement cascades into component shortages, production schedule slippage, inventory depletion, order fulfillment risk, and customer delivery delays.",
        "kpis": [
            {"id": "supplier_otd", "name": "Supplier On-Time Delivery", "query": "SELECT ROUND(COUNT(CASE WHEN SUPPLIER_DELIVERY_STATUS = 'On Time' THEN 1 END) * 100.0 / NULLIF(COUNT(CASE WHEN GR_DATE IS NOT NULL THEN 1 END), 0), 1) AS value FROM SCM_ANALYTICS.PERSONA.PROCUREMENT_PERSONA", "unit": "%", "description": "Percentage of supplier deliveries received on or before the committed date."},
            {"id": "avg_lead_time", "name": "Avg Procurement Lead Time", "query": "SELECT ROUND(AVG(PROCUREMENT_LEAD_TIME_DAYS), 1) AS value FROM SCM_ANALYTICS.PERSONA.PROCUREMENT_PERSONA WHERE GR_DATE IS NOT NULL", "unit": "days", "description": "Average number of days from PO creation to goods receipt."},
            {"id": "total_po_value", "name": "Total PO Value", "query": "SELECT ROUND(SUM(LINE_VALUE) / 1000000, 2) AS value FROM SCM_ANALYTICS.PERSONA.PROCUREMENT_PERSONA", "unit": "M USD", "description": "Total value of all purchase orders placed."},
            {"id": "supplier_rejection", "name": "Supplier Rejection Rate", "query": "SELECT ROUND(AVG(SUPPLIER_REJECTION_RATE_PCT), 1) AS value FROM SCM_ANALYTICS.PERSONA.PROCUREMENT_PERSONA WHERE INCOMING_REJECTED_QTY > 0", "unit": "%", "description": "Average rejection rate of incoming materials from suppliers."},
            {"id": "late_deliveries", "name": "Late Deliveries", "query": "SELECT COUNT(*) AS value FROM SCM_ANALYTICS.PERSONA.PROCUREMENT_PERSONA WHERE SUPPLIER_DELIVERY_STATUS LIKE 'Late%'", "unit": "orders", "description": "Number of supplier deliveries received after the promised date."},
            {"id": "active_suppliers", "name": "Active Suppliers", "query": "SELECT COUNT(DISTINCT SUPPLIER_NAME) AS value FROM SCM_ANALYTICS.PERSONA.PROCUREMENT_PERSONA", "unit": "", "description": "Number of distinct suppliers with active purchase orders."},
            {"id": "avg_unit_cost", "name": "Avg Component Cost", "query": "SELECT ROUND(AVG(PROCUREMENT_COST_PER_UNIT), 2) AS value FROM SCM_ANALYTICS.PERSONA.PROCUREMENT_PERSONA", "unit": "USD", "description": "Average unit procurement cost across all components."},
            {"id": "po_count", "name": "Total Purchase Orders", "query": "SELECT COUNT(DISTINCT PO_NUMBER) AS value FROM SCM_ANALYTICS.PERSONA.PROCUREMENT_PERSONA", "unit": "", "description": "Total number of purchase orders issued."}
        ],
        "charts": [
            {"id": "supplier_performance", "title": "Supplier Delivery Performance", "type": "bar", "query": "SELECT SUPPLIER_NAME AS label, ROUND(COUNT(CASE WHEN SUPPLIER_DELIVERY_STATUS = 'On Time' THEN 1 END) * 100.0 / NULLIF(COUNT(CASE WHEN GR_DATE IS NOT NULL THEN 1 END), 0), 1) AS value FROM SCM_ANALYTICS.PERSONA.PROCUREMENT_PERSONA GROUP BY SUPPLIER_NAME ORDER BY value ASC"},
            {"id": "lead_time_trend", "title": "Lead Time Trend by Month", "type": "line", "query": "SELECT PO_MONTH AS label, ROUND(AVG(PROCUREMENT_LEAD_TIME_DAYS), 1) AS value FROM SCM_ANALYTICS.PERSONA.PROCUREMENT_PERSONA WHERE GR_DATE IS NOT NULL GROUP BY PO_MONTH ORDER BY PO_MONTH"},
            {"id": "component_spend", "title": "Spend by Component Category", "type": "pie", "query": "SELECT COMPONENT_CATEGORY AS label, ROUND(SUM(LINE_VALUE), 0) AS value FROM SCM_ANALYTICS.PERSONA.PROCUREMENT_PERSONA GROUP BY COMPONENT_CATEGORY ORDER BY value DESC"},
            {"id": "rejection_by_supplier", "title": "Rejection Rate by Supplier", "type": "bar", "query": "SELECT SUPPLIER_NAME AS label, ROUND(SUM(INCOMING_REJECTED_QTY) * 100.0 / NULLIF(SUM(ORDER_QUANTITY), 0), 1) AS value FROM SCM_ANALYTICS.PERSONA.PROCUREMENT_PERSONA GROUP BY SUPPLIER_NAME HAVING SUM(INCOMING_REJECTED_QTY) > 0 ORDER BY value DESC"}
        ]
    },
    "manufacturing": {
        "id": "manufacturing",
        "name": "Manufacturing Manager",
        "view": "MANUFACTURING_PERSONA",
        "icon": "Factory",
        "description": "Overseeing laptop assembly operations, production efficiency, and quality yield.",
        "entity": "Production Order",
        "why_matters": "Transforms raw components into finished laptops. Manufacturing efficiency, yield rates, and cycle times determine product availability, cost structure, and ability to meet customer demand.",
        "upstream": ["Procurement", "Quality"],
        "downstream": ["Warehouse", "Logistics", "Sales", "Finance"],
        "cross_impact": "Production delays or quality failures reduce finished goods availability, creating inventory shortages that delay order fulfillment and customer deliveries.",
        "kpis": [
            {"id": "first_pass_yield", "name": "First Pass Yield", "query": "SELECT ROUND(AVG(FIRST_PASS_YIELD_PCT), 1) AS value FROM SCM_ANALYTICS.PERSONA.MANUFACTURING_PERSONA WHERE GOOD_QTY > 0", "unit": "%", "description": "Percentage of units passing quality on first attempt without rework."},
            {"id": "avg_cycle_time", "name": "Avg Cycle Time", "query": "SELECT ROUND(AVG(CYCLE_TIME_DAYS), 1) AS value FROM SCM_ANALYTICS.PERSONA.MANUFACTURING_PERSONA WHERE CYCLE_TIME_DAYS IS NOT NULL", "unit": "days", "description": "Average number of days to complete a production order."},
            {"id": "schedule_adherence", "name": "Schedule Adherence", "query": "SELECT ROUND(COUNT(CASE WHEN SCHEDULE_VARIANCE_DAYS <= 0 THEN 1 END) * 100.0 / NULLIF(COUNT(CASE WHEN ACTUAL_FINISH_DATE IS NOT NULL THEN 1 END), 0), 1) AS value FROM SCM_ANALYTICS.PERSONA.MANUFACTURING_PERSONA", "unit": "%", "description": "Percentage of production orders completed on or before planned finish date."},
            {"id": "total_produced", "name": "Total Units Produced", "query": "SELECT SUM(GOOD_QTY)::INT AS value FROM SCM_ANALYTICS.PERSONA.MANUFACTURING_PERSONA", "unit": "units", "description": "Total good units produced across all production orders."},
            {"id": "scrap_rate", "name": "Scrap Rate", "query": "SELECT ROUND(SUM(SCRAP_QTY) * 100.0 / NULLIF(SUM(PLANNED_QTY), 0), 2) AS value FROM SCM_ANALYTICS.PERSONA.MANUFACTURING_PERSONA", "unit": "%", "description": "Percentage of planned quantity lost as scrap during production."},
            {"id": "mto_ratio", "name": "Make-to-Order Ratio", "query": "SELECT ROUND(COUNT(CASE WHEN PRODUCTION_TYPE = 'Make-to-Order' THEN 1 END) * 100.0 / NULLIF(COUNT(*), 0), 1) AS value FROM SCM_ANALYTICS.PERSONA.MANUFACTURING_PERSONA", "unit": "%", "description": "Proportion of production orders triggered by customer sales orders."},
            {"id": "avg_mfg_cost", "name": "Avg Manufacturing Cost", "query": "SELECT ROUND(AVG(MANUFACTURING_COST_PER_UNIT), 2) AS value FROM SCM_ANALYTICS.PERSONA.MANUFACTURING_PERSONA WHERE MANUFACTURING_COST_PER_UNIT > 0", "unit": "USD", "description": "Average manufacturing cost per unit (materials + labor)."},
            {"id": "rejection_rate", "name": "Mfg Rejection Rate", "query": "SELECT ROUND(AVG(MANUFACTURING_REJECTION_RATE_PCT), 2) AS value FROM SCM_ANALYTICS.PERSONA.MANUFACTURING_PERSONA WHERE FINAL_TEST_FAILURES > 0", "unit": "%", "description": "Average final test failure rate in manufacturing."}
        ],
        "charts": [
            {"id": "yield_trend", "title": "First Pass Yield Trend", "type": "line", "query": "SELECT PRODUCTION_MONTH AS label, ROUND(AVG(FIRST_PASS_YIELD_PCT), 1) AS value FROM SCM_ANALYTICS.PERSONA.MANUFACTURING_PERSONA WHERE GOOD_QTY > 0 AND PRODUCTION_MONTH IS NOT NULL GROUP BY PRODUCTION_MONTH ORDER BY PRODUCTION_MONTH"},
            {"id": "production_by_product", "title": "Production Volume by Product", "type": "bar", "query": "SELECT PRODUCT_NAME AS label, SUM(GOOD_QTY)::INT AS value FROM SCM_ANALYTICS.PERSONA.MANUFACTURING_PERSONA GROUP BY PRODUCT_NAME ORDER BY value DESC"},
            {"id": "cycle_time_dist", "title": "Cycle Time by Product", "type": "bar", "query": "SELECT PRODUCT_NAME AS label, ROUND(AVG(CYCLE_TIME_DAYS), 1) AS value FROM SCM_ANALYTICS.PERSONA.MANUFACTURING_PERSONA WHERE CYCLE_TIME_DAYS IS NOT NULL GROUP BY PRODUCT_NAME ORDER BY value DESC"},
            {"id": "production_type_mix", "title": "Production Type Mix", "type": "pie", "query": "SELECT PRODUCTION_TYPE AS label, COUNT(*) AS value FROM SCM_ANALYTICS.PERSONA.MANUFACTURING_PERSONA GROUP BY PRODUCTION_TYPE"}
        ]
    },
    "warehouse": {
        "id": "warehouse",
        "name": "Warehouse Manager",
        "view": "WAREHOUSE_PERSONA",
        "icon": "Warehouse",
        "description": "Managing inventory levels, stock health, and storage operations for finished laptops.",
        "entity": "Inventory",
        "why_matters": "Acts as the buffer between production and customer fulfillment. Warehouse operations determine product availability, storage efficiency, and the speed at which orders can be picked, packed, and shipped.",
        "upstream": ["Manufacturing", "Quality"],
        "downstream": ["Sales", "Logistics", "Finance"],
        "cross_impact": "Inventory shortages in the warehouse directly block order fulfillment, causing backorders, delayed shipments, and lost customer satisfaction.",
        "kpis": [
            {"id": "total_inventory_value", "name": "Total Inventory Value", "query": "SELECT ROUND(SUM(BOOK_VALUE) / 1000000, 2) AS value FROM SCM_ANALYTICS.PERSONA.WAREHOUSE_PERSONA WHERE SNAPSHOT_DATE = (SELECT MAX(SNAPSHOT_DATE) FROM SCM_ANALYTICS.PERSONA.WAREHOUSE_PERSONA)", "unit": "M USD", "description": "Total book value of all inventory on hand."},
            {"id": "healthy_stock_pct", "name": "Healthy Stock Rate", "query": "SELECT ROUND(COUNT(CASE WHEN STOCK_HEALTH_STATUS = 'Healthy' THEN 1 END) * 100.0 / NULLIF(COUNT(*), 0), 1) AS value FROM SCM_ANALYTICS.PERSONA.WAREHOUSE_PERSONA WHERE SNAPSHOT_DATE = (SELECT MAX(SNAPSHOT_DATE) FROM SCM_ANALYTICS.PERSONA.WAREHOUSE_PERSONA)", "unit": "%", "description": "Percentage of SKUs with healthy stock levels."},
            {"id": "avg_utilization", "name": "Avg Storage Utilization", "query": "SELECT ROUND(AVG(STORAGE_UTILIZATION_PCT), 1) AS value FROM SCM_ANALYTICS.PERSONA.WAREHOUSE_PERSONA WHERE SNAPSHOT_DATE = (SELECT MAX(SNAPSHOT_DATE) FROM SCM_ANALYTICS.PERSONA.WAREHOUSE_PERSONA)", "unit": "%", "description": "Average storage rack utilization across all products."},
            {"id": "out_of_stock", "name": "Out of Stock Items", "query": "SELECT COUNT(*) AS value FROM SCM_ANALYTICS.PERSONA.WAREHOUSE_PERSONA WHERE STOCK_HEALTH_STATUS = 'Out of Stock' AND SNAPSHOT_DATE = (SELECT MAX(SNAPSHOT_DATE) FROM SCM_ANALYTICS.PERSONA.WAREHOUSE_PERSONA)", "unit": "items", "description": "Number of products with zero available stock."},
            {"id": "total_physical_stock", "name": "Total Physical Stock", "query": "SELECT SUM(PHYSICAL_STOCK_QTY)::INT AS value FROM SCM_ANALYTICS.PERSONA.WAREHOUSE_PERSONA WHERE SNAPSHOT_DATE = (SELECT MAX(SNAPSHOT_DATE) FROM SCM_ANALYTICS.PERSONA.WAREHOUSE_PERSONA)", "unit": "units", "description": "Total physical units in the warehouse."},
            {"id": "qc_hold_units", "name": "QC Hold Units", "query": "SELECT SUM(QC_HOLD_QTY)::INT AS value FROM SCM_ANALYTICS.PERSONA.WAREHOUSE_PERSONA WHERE SNAPSHOT_DATE = (SELECT MAX(SNAPSHOT_DATE) FROM SCM_ANALYTICS.PERSONA.WAREHOUSE_PERSONA)", "unit": "units", "description": "Units currently held for quality inspection."},
            {"id": "avg_turns", "name": "Avg Inventory Turns", "query": "SELECT ROUND(AVG(INVENTORY_TURNS_ANNUALIZED), 1) AS value FROM SCM_ANALYTICS.PERSONA.WAREHOUSE_PERSONA WHERE SNAPSHOT_DATE = (SELECT MAX(SNAPSHOT_DATE) FROM SCM_ANALYTICS.PERSONA.WAREHOUSE_PERSONA)", "unit": "x/year", "description": "Average annualized inventory turns across products."},
            {"id": "atp_units", "name": "Available to Promise", "query": "SELECT SUM(GREATEST(AVAILABLE_TO_PROMISE_QTY, 0))::INT AS value FROM SCM_ANALYTICS.PERSONA.WAREHOUSE_PERSONA WHERE SNAPSHOT_DATE = (SELECT MAX(SNAPSHOT_DATE) FROM SCM_ANALYTICS.PERSONA.WAREHOUSE_PERSONA)", "unit": "units", "description": "Total units available to promise for customer orders."}
        ],
        "charts": [
            {"id": "stock_health", "title": "Stock Health Distribution", "type": "pie", "query": "SELECT STOCK_HEALTH_STATUS AS label, COUNT(*) AS value FROM SCM_ANALYTICS.PERSONA.WAREHOUSE_PERSONA WHERE SNAPSHOT_DATE = (SELECT MAX(SNAPSHOT_DATE) FROM SCM_ANALYTICS.PERSONA.WAREHOUSE_PERSONA) GROUP BY STOCK_HEALTH_STATUS"},
            {"id": "inventory_by_product", "title": "Inventory by Product", "type": "bar", "query": "SELECT PRODUCT_NAME AS label, PHYSICAL_STOCK_QTY::INT AS value FROM SCM_ANALYTICS.PERSONA.WAREHOUSE_PERSONA WHERE SNAPSHOT_DATE = (SELECT MAX(SNAPSHOT_DATE) FROM SCM_ANALYTICS.PERSONA.WAREHOUSE_PERSONA) AND PRODUCT_CATEGORY = 'LAPTOP' ORDER BY value DESC"},
            {"id": "value_by_product", "title": "Inventory Value by Product", "type": "bar", "query": "SELECT PRODUCT_NAME AS label, ROUND(BOOK_VALUE, 0)::INT AS value FROM SCM_ANALYTICS.PERSONA.WAREHOUSE_PERSONA WHERE SNAPSHOT_DATE = (SELECT MAX(SNAPSHOT_DATE) FROM SCM_ANALYTICS.PERSONA.WAREHOUSE_PERSONA) AND PRODUCT_CATEGORY = 'LAPTOP' ORDER BY value DESC"},
            {"id": "utilization_trend", "title": "Storage Utilization by Product", "type": "bar", "query": "SELECT PRODUCT_NAME AS label, STORAGE_UTILIZATION_PCT AS value FROM SCM_ANALYTICS.PERSONA.WAREHOUSE_PERSONA WHERE SNAPSHOT_DATE = (SELECT MAX(SNAPSHOT_DATE) FROM SCM_ANALYTICS.PERSONA.WAREHOUSE_PERSONA) AND PRODUCT_CATEGORY = 'LAPTOP' ORDER BY value DESC"}
        ]
    },
    "sales": {
        "id": "sales",
        "name": "Sales Manager",
        "view": "SALES_PERSONA",
        "icon": "TrendingUp",
        "description": "Driving laptop revenue, managing customer relationships, and ensuring order fulfillment.",
        "entity": "Sales Order",
        "why_matters": "The revenue engine of the supply chain. Sales performance determines demand signals that drive production planning, inventory targets, and logistics capacity requirements.",
        "upstream": ["Warehouse", "Manufacturing"],
        "downstream": ["Logistics", "Finance", "Customer"],
        "cross_impact": "High sales demand without adequate inventory or production capacity leads to backorders, lost revenue, and damaged customer relationships.",
        "kpis": [
            {"id": "total_revenue", "name": "Total Revenue", "query": "SELECT ROUND(SUM(LINE_VALUE) / 1000000, 2) AS value FROM SCM_ANALYTICS.PERSONA.SALES_PERSONA", "unit": "M USD", "description": "Total revenue from all sales orders."},
            {"id": "on_time_delivery", "name": "On-Time Delivery", "query": "SELECT ROUND(COUNT(CASE WHEN ON_TIME_STATUS = 'On Time' THEN 1 END) * 100.0 / NULLIF(COUNT(CASE WHEN DELIVERY_DATE IS NOT NULL THEN 1 END), 0), 1) AS value FROM SCM_ANALYTICS.PERSONA.SALES_PERSONA", "unit": "%", "description": "Percentage of orders delivered on or before the promised date."},
            {"id": "fill_rate", "name": "Order Fill Rate", "query": "SELECT ROUND(AVG(LINE_FILL_RATE_PCT), 1) AS value FROM SCM_ANALYTICS.PERSONA.SALES_PERSONA WHERE QUANTITY_SHIPPED > 0", "unit": "%", "description": "Average percentage of ordered quantity fulfilled."},
            {"id": "total_orders", "name": "Total Orders", "query": "SELECT COUNT(DISTINCT ORDER_ID) AS value FROM SCM_ANALYTICS.PERSONA.SALES_PERSONA", "unit": "", "description": "Total number of customer sales orders."},
            {"id": "avg_order_value", "name": "Avg Order Value", "query": "SELECT ROUND(AVG(TOTAL_ORDER_VALUE), 0) AS value FROM (SELECT DISTINCT ORDER_ID, TOTAL_ORDER_VALUE FROM SCM_ANALYTICS.PERSONA.SALES_PERSONA)", "unit": "USD", "description": "Average value per sales order."},
            {"id": "avg_lead_time", "name": "Avg Sales Lead Time", "query": "SELECT ROUND(AVG(SALES_LEAD_TIME_DAYS), 1) AS value FROM SCM_ANALYTICS.PERSONA.SALES_PERSONA WHERE DELIVERY_DATE IS NOT NULL", "unit": "days", "description": "Average days from order creation to customer delivery."},
            {"id": "backorder_count", "name": "Backordered Items", "query": "SELECT COUNT(*) AS value FROM SCM_ANALYTICS.PERSONA.SALES_PERSONA WHERE ON_TIME_STATUS = 'Backordered'", "unit": "", "description": "Number of line items currently backordered."},
            {"id": "customer_count", "name": "Active Customers", "query": "SELECT COUNT(DISTINCT CUSTOMER_NAME) AS value FROM SCM_ANALYTICS.PERSONA.SALES_PERSONA", "unit": "", "description": "Number of distinct customers with orders."}
        ],
        "charts": [
            {"id": "revenue_trend", "title": "Monthly Revenue Trend", "type": "line", "query": "SELECT ORDER_MONTH AS label, ROUND(SUM(LINE_VALUE), 0) AS value FROM SCM_ANALYTICS.PERSONA.SALES_PERSONA GROUP BY ORDER_MONTH ORDER BY ORDER_MONTH"},
            {"id": "delivery_performance", "title": "Delivery Performance", "type": "pie", "query": "SELECT ON_TIME_STATUS AS label, COUNT(*) AS value FROM SCM_ANALYTICS.PERSONA.SALES_PERSONA WHERE DELIVERY_DATE IS NOT NULL GROUP BY ON_TIME_STATUS"},
            {"id": "revenue_by_product", "title": "Revenue by Product", "type": "bar", "query": "SELECT PRODUCT_NAME AS label, ROUND(SUM(LINE_VALUE), 0) AS value FROM SCM_ANALYTICS.PERSONA.SALES_PERSONA WHERE PRODUCT_CATEGORY = 'LAPTOP' GROUP BY PRODUCT_NAME ORDER BY value DESC"},
            {"id": "orders_by_country", "title": "Orders by Country", "type": "bar", "query": "SELECT CUSTOMER_COUNTRY AS label, COUNT(DISTINCT ORDER_ID) AS value FROM SCM_ANALYTICS.PERSONA.SALES_PERSONA GROUP BY CUSTOMER_COUNTRY ORDER BY value DESC"}
        ]
    },
    "logistics": {
        "id": "logistics",
        "name": "Logistics Manager",
        "view": "LOGISTICS_PERSONA",
        "icon": "Truck",
        "description": "Managing outbound shipments, carrier performance, and delivery to customers.",
        "entity": "Shipment",
        "why_matters": "The last mile of the supply chain connecting warehouse to customer. Logistics efficiency determines delivery speed, cost, and the customer's final experience with the brand.",
        "upstream": ["Warehouse", "Sales"],
        "downstream": ["Customer", "Finance"],
        "cross_impact": "Logistics delays or carrier failures directly impact customer delivery promises, creating dissatisfaction and potential revenue loss from returns or cancellations.",
        "kpis": [
            {"id": "otd_rate", "name": "On-Time Delivery Rate", "query": "SELECT ROUND(COUNT(CASE WHEN DELIVERY_PERFORMANCE = 'On Time' THEN 1 END) * 100.0 / NULLIF(COUNT(*), 0), 1) AS value FROM SCM_ANALYTICS.PERSONA.LOGISTICS_PERSONA WHERE DELIVERY_DATE IS NOT NULL", "unit": "%", "description": "Percentage of shipments delivered on or before customer promise date."},
            {"id": "avg_transit_time", "name": "Avg Transit Time", "query": "SELECT ROUND(AVG(TRANSIT_TIME_DAYS), 1) AS value FROM SCM_ANALYTICS.PERSONA.LOGISTICS_PERSONA WHERE TRANSIT_TIME_DAYS IS NOT NULL", "unit": "days", "description": "Average transit time from dispatch to delivery."},
            {"id": "total_shipments", "name": "Total Shipments", "query": "SELECT COUNT(DISTINCT SHIPMENT_NUMBER) AS value FROM SCM_ANALYTICS.PERSONA.LOGISTICS_PERSONA", "unit": "", "description": "Total number of shipments dispatched."},
            {"id": "late_shipments", "name": "Late Shipments", "query": "SELECT COUNT(*) AS value FROM SCM_ANALYTICS.PERSONA.LOGISTICS_PERSONA WHERE DELIVERY_PERFORMANCE = 'Late'", "unit": "", "description": "Number of shipments delivered after the promised date."},
            {"id": "active_carriers", "name": "Active Carriers", "query": "SELECT COUNT(DISTINCT CARRIER_NAME) AS value FROM SCM_ANALYTICS.PERSONA.LOGISTICS_PERSONA", "unit": "", "description": "Number of carriers handling shipments."},
            {"id": "countries_served", "name": "Countries Served", "query": "SELECT COUNT(DISTINCT DELIVERY_COUNTRY) AS value FROM SCM_ANALYTICS.PERSONA.LOGISTICS_PERSONA", "unit": "", "description": "Number of distinct countries with deliveries."},
            {"id": "avg_days_late", "name": "Avg Days Late (when late)", "query": "SELECT ROUND(AVG(DAYS_VS_PROMISE), 1) AS value FROM SCM_ANALYTICS.PERSONA.LOGISTICS_PERSONA WHERE DELIVERY_PERFORMANCE = 'Late'", "unit": "days", "description": "Average number of days past promise when delivery is late."},
            {"id": "total_weight", "name": "Total Shipped Weight", "query": "SELECT ROUND(SUM(SHIPMENT_WEIGHT_KG), 0) AS value FROM SCM_ANALYTICS.PERSONA.LOGISTICS_PERSONA", "unit": "kg", "description": "Total weight of all shipped goods."}
        ],
        "charts": [
            {"id": "carrier_performance", "title": "Carrier On-Time Performance", "type": "bar", "query": "SELECT CARRIER_NAME AS label, ROUND(COUNT(CASE WHEN DELIVERY_PERFORMANCE = 'On Time' THEN 1 END) * 100.0 / NULLIF(COUNT(*), 0), 1) AS value FROM SCM_ANALYTICS.PERSONA.LOGISTICS_PERSONA WHERE DELIVERY_DATE IS NOT NULL GROUP BY CARRIER_NAME ORDER BY value ASC"},
            {"id": "transit_time_trend", "title": "Transit Time Trend", "type": "line", "query": "SELECT DELIVERY_MONTH AS label, ROUND(AVG(TRANSIT_TIME_DAYS), 1) AS value FROM SCM_ANALYTICS.PERSONA.LOGISTICS_PERSONA WHERE DELIVERY_MONTH IS NOT NULL GROUP BY DELIVERY_MONTH ORDER BY DELIVERY_MONTH"},
            {"id": "deliveries_by_country", "title": "Deliveries by Country", "type": "pie", "query": "SELECT DELIVERY_COUNTRY AS label, COUNT(*) AS value FROM SCM_ANALYTICS.PERSONA.LOGISTICS_PERSONA GROUP BY DELIVERY_COUNTRY ORDER BY value DESC"},
            {"id": "status_distribution", "title": "Logistics Status", "type": "pie", "query": "SELECT LOGISTICS_STATUS AS label, COUNT(*) AS value FROM SCM_ANALYTICS.PERSONA.LOGISTICS_PERSONA GROUP BY LOGISTICS_STATUS"}
        ]
    },
    "quality": {
        "id": "quality",
        "name": "Quality Manager",
        "view": "QUALITY_PERSONA",
        "icon": "Shield",
        "description": "Ensuring product quality through incoming inspections and final testing.",
        "entity": "Quality Notification",
        "why_matters": "The gatekeeper ensuring only conforming materials enter production and only quality products reach customers. Quality failures at any stage create waste, delays, and customer dissatisfaction.",
        "upstream": ["Procurement", "Manufacturing"],
        "downstream": ["Warehouse", "Sales", "Customer"],
        "cross_impact": "Quality holds block inventory availability, while high rejection rates force procurement to re-source and manufacturing to rework, delaying the entire supply chain.",
        "kpis": [
            {"id": "incoming_rejection", "name": "Incoming Rejection Rate", "query": "SELECT ROUND(AVG(REJECTION_RATE_PCT), 1) AS value FROM SCM_ANALYTICS.PERSONA.QUALITY_PERSONA WHERE INSPECTION_TYPE = 'Incoming Inspection'", "unit": "%", "description": "Average rejection rate for incoming material inspections."},
            {"id": "final_test_rejection", "name": "Final Test Rejection Rate", "query": "SELECT ROUND(AVG(REJECTION_RATE_PCT), 1) AS value FROM SCM_ANALYTICS.PERSONA.QUALITY_PERSONA WHERE INSPECTION_TYPE = 'Final Test'", "unit": "%", "description": "Average rejection rate during final product testing."},
            {"id": "total_notifications", "name": "Total Quality Notifications", "query": "SELECT COUNT(DISTINCT NOTIFICATION_NUMBER) AS value FROM SCM_ANALYTICS.PERSONA.QUALITY_PERSONA", "unit": "", "description": "Total quality notifications raised."},
            {"id": "total_rejected_qty", "name": "Total Rejected Qty", "query": "SELECT SUM(REJECTED_QTY)::INT AS value FROM SCM_ANALYTICS.PERSONA.QUALITY_PERSONA", "unit": "units", "description": "Total quantity of materials/products rejected."},
            {"id": "incoming_count", "name": "Incoming Inspections", "query": "SELECT COUNT(*) AS value FROM SCM_ANALYTICS.PERSONA.QUALITY_PERSONA WHERE INSPECTION_TYPE = 'Incoming Inspection'", "unit": "", "description": "Number of incoming material inspections performed."},
            {"id": "final_test_count", "name": "Final Tests", "query": "SELECT COUNT(*) AS value FROM SCM_ANALYTICS.PERSONA.QUALITY_PERSONA WHERE INSPECTION_TYPE = 'Final Test'", "unit": "", "description": "Number of final product tests performed."},
            {"id": "top_defect_material", "name": "Most Rejected Material", "query": "SELECT MATERIAL_NAME AS value FROM SCM_ANALYTICS.PERSONA.QUALITY_PERSONA GROUP BY MATERIAL_NAME ORDER BY SUM(REJECTED_QTY) DESC LIMIT 1", "unit": "", "description": "Material with the highest total rejected quantity."},
            {"id": "qc_hold_impact", "name": "QC Hold Stock", "query": "SELECT COALESCE(SUM(CURRENT_QC_HOLD_QTY), 0)::INT AS value FROM (SELECT DISTINCT MATERIAL_CODE, CURRENT_QC_HOLD_QTY FROM SCM_ANALYTICS.PERSONA.QUALITY_PERSONA WHERE CURRENT_QC_HOLD_QTY IS NOT NULL) t", "unit": "units", "description": "Current inventory held for quality inspection."}
        ],
        "charts": [
            {"id": "rejection_trend", "title": "Rejection Rate Trend", "type": "line", "query": "SELECT INSPECTION_MONTH AS label, ROUND(AVG(REJECTION_RATE_PCT), 1) AS value FROM SCM_ANALYTICS.PERSONA.QUALITY_PERSONA WHERE INSPECTION_MONTH IS NOT NULL GROUP BY INSPECTION_MONTH ORDER BY INSPECTION_MONTH"},
            {"id": "by_type", "title": "Notifications by Inspection Type", "type": "pie", "query": "SELECT INSPECTION_TYPE AS label, COUNT(*) AS value FROM SCM_ANALYTICS.PERSONA.QUALITY_PERSONA GROUP BY INSPECTION_TYPE"},
            {"id": "by_material", "title": "Rejected Qty by Material", "type": "bar", "query": "SELECT MATERIAL_NAME AS label, SUM(REJECTED_QTY)::INT AS value FROM SCM_ANALYTICS.PERSONA.QUALITY_PERSONA GROUP BY MATERIAL_NAME ORDER BY value DESC LIMIT 10"},
            {"id": "by_supplier", "title": "Incoming Rejections by Supplier", "type": "bar", "query": "SELECT SUPPLIER_NAME AS label, SUM(REJECTED_QTY)::INT AS value FROM SCM_ANALYTICS.PERSONA.QUALITY_PERSONA WHERE INSPECTION_TYPE = 'Incoming Inspection' AND SUPPLIER_NAME IS NOT NULL GROUP BY SUPPLIER_NAME ORDER BY value DESC"}
        ]
    },
    "finance": {
        "id": "finance",
        "name": "Finance Manager",
        "view": "FINANCE_PERSONA",
        "icon": "DollarSign",
        "description": "Managing profitability, cost control, and financial performance of the laptop business.",
        "entity": "Financial Transaction",
        "why_matters": "Provides the financial lens across the entire supply chain. Finance tracks revenue, costs, margins, and inventory valuation to ensure the business remains profitable and cash-flow positive.",
        "upstream": ["Sales", "Procurement", "Manufacturing", "Logistics"],
        "downstream": ["Executive Leadership"],
        "cross_impact": "Financial constraints or margin erosion can trigger cost-cutting in procurement (cheaper suppliers), reduced production capacity, or logistics downgrades that impact service quality.",
        "kpis": [
            {"id": "total_revenue", "name": "Total Revenue", "query": "SELECT ROUND(SUM(REVENUE) / 1000000, 2) AS value FROM SCM_ANALYTICS.PERSONA.FINANCE_PERSONA", "unit": "M USD", "description": "Total revenue across all orders."},
            {"id": "gross_margin", "name": "Avg Gross Margin", "query": "SELECT ROUND(AVG(GROSS_MARGIN_PCT), 1) AS value FROM SCM_ANALYTICS.PERSONA.FINANCE_PERSONA WHERE GROSS_MARGIN_PCT IS NOT NULL", "unit": "%", "description": "Average gross margin percentage across all orders."},
            {"id": "total_landed_cost", "name": "Total Landed Cost", "query": "SELECT ROUND(SUM(TOTAL_LANDED_COST) / 1000000, 2) AS value FROM SCM_ANALYTICS.PERSONA.FINANCE_PERSONA", "unit": "M USD", "description": "Total landed cost including materials, labor, freight, and duty."},
            {"id": "gross_profit", "name": "Total Gross Profit", "query": "SELECT ROUND(SUM(GROSS_PROFIT) / 1000000, 2) AS value FROM SCM_ANALYTICS.PERSONA.FINANCE_PERSONA", "unit": "M USD", "description": "Total gross profit (revenue minus landed cost)."},
            {"id": "avg_landed_cost_unit", "name": "Avg Landed Cost/Unit", "query": "SELECT ROUND(AVG(LANDED_COST_PER_UNIT), 2) AS value FROM SCM_ANALYTICS.PERSONA.FINANCE_PERSONA WHERE LANDED_COST_PER_UNIT IS NOT NULL", "unit": "USD", "description": "Average landed cost per unit sold."},
            {"id": "inventory_value", "name": "Inventory Book Value", "query": "SELECT ROUND(AVG(INVENTORY_BOOK_VALUE) / 1000, 1) AS value FROM SCM_ANALYTICS.PERSONA.FINANCE_PERSONA WHERE INVENTORY_BOOK_VALUE > 0", "unit": "K USD", "description": "Average inventory book value across periods."},
            {"id": "avg_turns", "name": "Avg Inventory Turns", "query": "SELECT ROUND(AVG(INVENTORY_TURNS_ANNUALIZED), 1) AS value FROM SCM_ANALYTICS.PERSONA.FINANCE_PERSONA", "unit": "x/year", "description": "Average annualized inventory turns."},
            {"id": "freight_pct", "name": "Freight Cost %", "query": "SELECT ROUND(SUM(COST_FREIGHT) * 100.0 / NULLIF(SUM(TOTAL_LANDED_COST), 0), 1) AS value FROM SCM_ANALYTICS.PERSONA.FINANCE_PERSONA", "unit": "%", "description": "Freight cost as percentage of total landed cost."}
        ],
        "charts": [
            {"id": "revenue_trend", "title": "Monthly Revenue Trend", "type": "line", "query": "SELECT REVENUE_MONTH AS label, ROUND(SUM(REVENUE), 0) AS value FROM SCM_ANALYTICS.PERSONA.FINANCE_PERSONA WHERE REVENUE_MONTH IS NOT NULL GROUP BY REVENUE_MONTH ORDER BY REVENUE_MONTH"},
            {"id": "margin_by_product", "title": "Gross Margin by Product", "type": "bar", "query": "SELECT PRODUCT_NAME AS label, ROUND(AVG(GROSS_MARGIN_PCT), 1) AS value FROM SCM_ANALYTICS.PERSONA.FINANCE_PERSONA GROUP BY PRODUCT_NAME ORDER BY value DESC"},
            {"id": "cost_breakdown", "title": "Cost Breakdown", "type": "pie", "query": "SELECT 'Materials' AS label, ROUND(SUM(COST_MATERIALS), 0) AS value FROM SCM_ANALYTICS.PERSONA.FINANCE_PERSONA UNION ALL SELECT 'Labor', ROUND(SUM(COST_LABOR), 0) FROM SCM_ANALYTICS.PERSONA.FINANCE_PERSONA UNION ALL SELECT 'Freight', ROUND(SUM(COST_FREIGHT), 0) FROM SCM_ANALYTICS.PERSONA.FINANCE_PERSONA UNION ALL SELECT 'Duty', ROUND(SUM(COST_DUTY), 0) FROM SCM_ANALYTICS.PERSONA.FINANCE_PERSONA"},
            {"id": "revenue_by_customer", "title": "Revenue by Top Customers", "type": "bar", "query": "SELECT CUSTOMER_NAME AS label, ROUND(SUM(REVENUE), 0) AS value FROM SCM_ANALYTICS.PERSONA.FINANCE_PERSONA GROUP BY CUSTOMER_NAME ORDER BY value DESC LIMIT 8"}
        ]
    }
}

ONTOLOGY_CONFIG = {
    "entities": [
        {"id": "supplier", "name": "Supplier", "description": "Provides raw materials and components", "stage": 1},
        {"id": "component", "name": "Component", "description": "Raw materials and parts for laptop assembly", "stage": 2},
        {"id": "procurement", "name": "Procurement", "description": "Manages purchasing and supplier relationships", "stage": 3},
        {"id": "quality_incoming", "name": "Quality (Incoming)", "description": "Inspects incoming materials", "stage": 4},
        {"id": "manufacturing", "name": "Manufacturing", "description": "Assembles laptops from components", "stage": 6},
        {"id": "quality_final", "name": "Quality (Final Test)", "description": "Tests finished products", "stage": 7},
        {"id": "warehouse", "name": "Warehouse", "description": "Stores finished goods inventory", "stage": 8},
        {"id": "sales", "name": "Sales", "description": "Manages customer orders and demand", "stage": 9},
        {"id": "logistics", "name": "Logistics", "description": "Ships products to customers", "stage": 10},
        {"id": "customer", "name": "Customer", "description": "End recipient of laptop products", "stage": 11},
        {"id": "finance", "name": "Finance", "description": "Monitors costs, revenue, and profitability", "stage": 0}
    ],
    "relationships": [
        {"source": "supplier", "target": "component", "relationship": "SUPPLIES"},
        {"source": "component", "target": "procurement", "relationship": "PURCHASED_BY"},
        {"source": "procurement", "target": "quality_incoming", "relationship": "INSPECTED_BY"},
        {"source": "quality_incoming", "target": "manufacturing", "relationship": "RELEASED_TO"},
        {"source": "manufacturing", "target": "quality_final", "relationship": "TESTED_BY"},
        {"source": "quality_final", "target": "warehouse", "relationship": "RELEASED_TO"},
        {"source": "warehouse", "target": "sales", "relationship": "FULFILLS"},
        {"source": "sales", "target": "logistics", "relationship": "SHIPPED_BY"},
        {"source": "logistics", "target": "customer", "relationship": "DELIVERS_TO"},
        {"source": "finance", "target": "procurement", "relationship": "BUDGETS"},
        {"source": "finance", "target": "manufacturing", "relationship": "COST_CONTROLS"},
        {"source": "finance", "target": "logistics", "relationship": "FREIGHT_COSTS"}
    ],
    "personas_to_entities": {
        "procurement": ["supplier", "component", "procurement"],
        "manufacturing": ["manufacturing", "component"],
        "warehouse": ["warehouse"],
        "sales": ["sales", "customer"],
        "logistics": ["logistics", "customer"],
        "quality": ["quality_incoming", "quality_final"],
        "finance": ["finance", "procurement", "manufacturing", "sales", "logistics"]
    }
}
