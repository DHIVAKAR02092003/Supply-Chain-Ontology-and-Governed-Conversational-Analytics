-- =====================================================
-- Supply Chain Ontology Definitions
-- =====================================================
-- This file documents the ontology relationships that
-- underpin the governed analytics layer.

-- Ontology Entity Registry
CREATE TABLE IF NOT EXISTS SCM_ANALYTICS.PERSONA.ONTOLOGY_ENTITIES (
    entity_id VARCHAR(50) PRIMARY KEY,
    entity_name VARCHAR(100),
    entity_description VARCHAR(500),
    stage_order INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

INSERT INTO SCM_ANALYTICS.PERSONA.ONTOLOGY_ENTITIES VALUES
('supplier', 'Supplier', 'Provides raw materials and components for laptop manufacturing', 1, CURRENT_TIMESTAMP()),
('component', 'Component', 'Raw materials and parts needed for laptop assembly', 2, CURRENT_TIMESTAMP()),
('procurement', 'Procurement', 'Manages purchasing and supplier relationships', 3, CURRENT_TIMESTAMP()),
('quality_incoming', 'Quality (Incoming)', 'Inspects incoming materials from suppliers', 4, CURRENT_TIMESTAMP()),
('planning', 'Planning', 'Balances demand forecasts with production capacity', 5, CURRENT_TIMESTAMP()),
('manufacturing', 'Manufacturing', 'Assembles laptops from components', 6, CURRENT_TIMESTAMP()),
('quality_final', 'Quality (Final Test)', 'Tests finished laptop products before shipment', 7, CURRENT_TIMESTAMP()),
('warehouse', 'Warehouse', 'Stores finished goods inventory', 8, CURRENT_TIMESTAMP()),
('sales', 'Sales', 'Manages customer orders and revenue', 9, CURRENT_TIMESTAMP()),
('logistics', 'Logistics', 'Ships products to customers', 10, CURRENT_TIMESTAMP()),
('customer', 'Customer', 'End recipient of laptop products', 11, CURRENT_TIMESTAMP()),
('finance', 'Finance', 'Monitors costs, revenue, and profitability across all stages', 0, CURRENT_TIMESTAMP());

-- Ontology Relationships
CREATE TABLE IF NOT EXISTS SCM_ANALYTICS.PERSONA.ONTOLOGY_RELATIONSHIPS (
    source_entity VARCHAR(50),
    target_entity VARCHAR(50),
    relationship_type VARCHAR(50),
    description VARCHAR(200),
    FOREIGN KEY (source_entity) REFERENCES SCM_ANALYTICS.PERSONA.ONTOLOGY_ENTITIES(entity_id),
    FOREIGN KEY (target_entity) REFERENCES SCM_ANALYTICS.PERSONA.ONTOLOGY_ENTITIES(entity_id)
);

INSERT INTO SCM_ANALYTICS.PERSONA.ONTOLOGY_RELATIONSHIPS VALUES
('supplier', 'component', 'SUPPLIES', 'Supplier provides components to procurement'),
('component', 'procurement', 'PURCHASED_BY', 'Components are purchased through procurement'),
('procurement', 'quality_incoming', 'INSPECTED_BY', 'Procured materials go through incoming inspection'),
('quality_incoming', 'manufacturing', 'RELEASED_TO', 'Approved materials released to production'),
('planning', 'manufacturing', 'SCHEDULES', 'Planning determines production schedules'),
('manufacturing', 'quality_final', 'TESTED_BY', 'Finished goods undergo final testing'),
('quality_final', 'warehouse', 'RELEASED_TO', 'Tested products released to warehouse'),
('warehouse', 'sales', 'FULFILLS', 'Warehouse inventory fulfills customer orders'),
('sales', 'logistics', 'SHIPPED_BY', 'Sales orders trigger logistics shipments'),
('logistics', 'customer', 'DELIVERS_TO', 'Logistics delivers to customer'),
('sales', 'planning', 'DEMAND_SIGNAL', 'Sales demand signals drive planning forecasts'),
('finance', 'procurement', 'BUDGETS', 'Finance controls procurement budgets'),
('finance', 'manufacturing', 'COST_CONTROLS', 'Finance monitors manufacturing costs'),
('finance', 'logistics', 'FREIGHT_COSTS', 'Finance tracks logistics costs');

-- Canonical Metric Definitions
CREATE TABLE IF NOT EXISTS SCM_ANALYTICS.PERSONA.CANONICAL_METRICS (
    metric_id VARCHAR(50) PRIMARY KEY,
    metric_name VARCHAR(100),
    definition VARCHAR(500),
    formula VARCHAR(500),
    used_by_personas VARCHAR(200)
);

INSERT INTO SCM_ANALYTICS.PERSONA.CANONICAL_METRICS VALUES
('on_time_delivery', 'On-Time Delivery', 'Percentage of deliveries completed on or before the committed delivery date.', 'COUNT(on_time) / COUNT(total_delivered) * 100', 'Procurement, Sales, Logistics'),
('fill_rate', 'Fill Rate', 'Percentage of requested or ordered quantity successfully fulfilled.', 'SUM(delivered_qty) / SUM(ordered_qty) * 100', 'Sales, Warehouse'),
('days_of_inventory', 'Days of Inventory', 'Average number of days current inventory can support expected demand.', 'current_stock / (daily_demand)', 'Planning, Warehouse, Finance'),
('landed_cost', 'Landed Cost', 'Total cost of acquiring and delivering a product including purchase, transportation, handling, and duties.', 'material_cost + labor_cost + freight_cost + duty_cost', 'Finance, Procurement'),
('first_pass_yield', 'First Pass Yield', 'Percentage of units passing quality on first attempt without rework.', 'good_qty / total_qty * 100', 'Manufacturing, Quality'),
('capacity_utilization', 'Capacity Utilization', 'Percentage of available production capacity currently in use.', 'used_hours / available_hours * 100', 'Planning, Manufacturing'),
('forecast_accuracy', 'Forecast Accuracy', 'How closely demand forecasts match actual demand signals.', '1 - ABS(forecast - actual) / forecast', 'Planning'),
('gross_margin', 'Gross Margin', 'Revenue minus landed cost as a percentage of revenue.', '(revenue - landed_cost) / revenue * 100', 'Finance, Sales');
