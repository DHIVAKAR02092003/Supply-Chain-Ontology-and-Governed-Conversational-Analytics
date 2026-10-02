# Supply Chain Document Templates for PDF Generation

Use these contents to generate 5 PDF documents (each ~5 pages). All data references real entities from the Snowflake database.

---

## DOCUMENT 1: Supplier Quality Assessment Report

**Filename:** `SQA-RPT-2025-Q3-PowerCell.pdf`

### Page 1 — Cover

```
TECHNOVA ELECTRONICS INC.
SUPPLIER QUALITY ASSESSMENT REPORT

Supplier: PowerCell Technologies
Location: Shenzhen, China
Assessment Period: July - September 2025 (Q3)
Report ID: SQA-RPT-2025-Q3-001
Prepared by: Quality Engineering Team
Classification: CONFIDENTIAL
Date: October 5, 2025
```

### Page 2 — Executive Summary & Supplier Profile

```
EXECUTIVE SUMMARY

PowerCell Technologies has been assessed as a HIGH RISK supplier for Q3 2025.
On-time delivery performance has dropped to 73.2%, significantly below the
target threshold of 95%. The average procurement lead time of 11.1 days exceeds
the contractual commitment of 8 days. While the incoming material rejection rate
of 1.0% remains within tolerance, delivery reliability continues to impact
downstream manufacturing schedules at the Austin Assembly Plant.

SUPPLIER PROFILE

Company Name: PowerCell Technologies
Headquarters: Shenzhen, China
Components Supplied: Li-Ion Battery Cell 72Wh, Li-Ion Battery Cell 56Wh, NVMe SSD 1TB M.2
Total PO Lines (Q3): 56
Industry Sector: Electronics
Relationship Since: 2022
Tier: Tier 1 Strategic Supplier

RISK CLASSIFICATION: RED
Criteria: OTD below 85% triggers RED classification per Policy POL-RISK-004.
```

### Page 3 — Performance Metrics

```
DELIVERY PERFORMANCE

On-Time Delivery Rate: 73.2% (Target: >= 95%)
Average Lead Time: 11.1 days (Contractual: 8 days)
Late Delivery Count: 15 out of 56 PO lines
Worst Delay: 7 days (PO00000198, Li-Ion Battery Cell 72Wh)

Delivery performance has declined from 81% in Q2 to 73.2% in Q3.
Root cause analysis indicates capacity constraints at the Shenzhen facility
due to increased demand from multiple OEM customers.

QUALITY PERFORMANCE

Incoming Rejection Rate: 1.0% (Target: < 2%)
Total Units Rejected: 14 units across all components
Most Common Defect: Cell voltage below threshold (Li-Ion Battery Cell 72Wh)
Quality Notifications Raised: 5

Although quality metrics remain within acceptable limits, the combination
of delivery delays and quality holds has created compounding effects on
the Austin Assembly Plant production schedule.

COST PERFORMANCE

Average Unit Price (Battery 72Wh): $400.00
Average Unit Price (Battery 56Wh): $350.00
Average Unit Price (SSD 1TB): $120.00
Price variance vs contract: Within 2% tolerance
Invoice match rate: 94% (6% with value discrepancies requiring resolution)
```

### Page 4 — Impact Analysis

```
DOWNSTREAM IMPACT ASSESSMENT

Manufacturing Impact:
PowerCell's delayed battery deliveries directly caused 3 production order
reschedulings in August 2025. The TechNova ProBook 15 Laptop (FG-LP-PRO15)
was most affected, with cycle time increasing from 2.0 to 2.8 days during
the affected period due to component unavailability.

Inventory Impact:
Battery component stock at Austin Finished Goods Warehouse dropped below
safety stock level twice during Q3. The Li-Ion Battery Cell 72Wh reached
critical low status on August 12 and September 3.

Customer Impact:
12 customer sales orders experienced delayed fulfillment traceable to
PowerCell delivery delays. Average customer delivery delay: 3.2 days.
Affected customers include Ravi Kumar (Bangalore), Infovista Corp (New York),
and QuantumLeap Ltd (Chicago).

Financial Impact:
Estimated cost of disruption: $45,000
- Expedited freight for alternative sourcing: $12,000
- Production overtime at Austin plant: $18,000
- Customer credit notes for late delivery: $15,000
```

### Page 5 — Corrective Actions & Recommendations

```
CORRECTIVE ACTION PLAN

1. IMMEDIATE (Within 2 weeks):
   - PowerCell to provide daily shipment tracking for all open POs
   - Establish safety stock buffer of 200 units for Battery 72Wh
   - Activate secondary supplier LuminaDisplay Corp for SSD components

2. SHORT-TERM (Within 30 days):
   - PowerCell to complete root cause analysis for delivery failures
   - Implement weekly supplier performance review calls
   - PowerCell to add dedicated production line for TechNova orders

3. LONG-TERM (Within 90 days):
   - Evaluate dual-sourcing strategy for all battery components
   - PowerCell to invest in capacity expansion (committed Q1 2026)
   - Renegotiate contractual lead time penalties

ESCALATION:
If OTD does not improve to 85% by end of Q4 2025, recommendation is to
reduce PowerCell allocation by 30% and redistribute to ChipWorks
Semiconductor (current OTD: 94.3%) and LuminaDisplay Corp (current OTD: 94.3%).

APPROVAL SIGNATURES:
Quality Manager: _______________  Date: ___________
Procurement Director: __________  Date: ___________
VP Supply Chain: _______________  Date: ___________
```

---

## DOCUMENT 2: Production Deviation Report

**Filename:** `PDR-2025-08-WRK16-Assembly.pdf`

### Page 1 — Cover

```
TECHNOVA ELECTRONICS INC.
PRODUCTION DEVIATION REPORT

Product: TechNova WorkStation 16 Laptop (FG-LP-WRK16)
Plant: Austin Assembly Plant
Deviation Period: August 1-31, 2025
Report ID: PDR-2025-08-001
Prepared by: Manufacturing Engineering
Classification: INTERNAL USE ONLY
Date: September 10, 2025
```

### Page 2 — Deviation Summary

```
DEVIATION SUMMARY

The TechNova WorkStation 16 Laptop experienced the lowest first pass yield
of all laptop models during August 2025, averaging 90.2% against a target
of 97%. This represents a significant deviation requiring root cause
analysis and corrective action.

PRODUCTION OVERVIEW (WorkStation 16)

Total Production Orders: 87
Total Planned Quantity: 1,198 units
Good Quantity Produced: 1,135 units
Scrap Quantity: 5 units
Rework Quantity: 58 units
Average Cycle Time: 2.0 days
Schedule Variance: +0.3 days average delay
Production Type Split: 18% Make-to-Order, 82% Batch Production

COMPARISON WITH OTHER MODELS

Product                          | First Pass Yield | Cycle Time
TechNova AirBook 13 Laptop      | 99.6%            | 1.9 days
TechNova EduBook 14 Laptop      | 95.9%            | 2.0 days
TechNova ProBook 15 Laptop      | 94.9%            | 2.0 days
TechNova ProBook 14 Laptop      | 91.1%            | 2.1 days
TechNova WorkStation 16 Laptop  | 90.2%            | 2.0 days  ** DEVIATION **

The WorkStation 16 yield is 9.4 percentage points below the AirBook 13,
indicating a model-specific assembly issue rather than a systemic plant problem.
```

### Page 3 — Root Cause Analysis

```
ROOT CAUSE ANALYSIS

Primary Root Cause: Motherboard-to-chassis alignment tolerance

The WorkStation 16 uses a larger 16-inch chassis (Aluminum Chassis 16in)
with tighter thermal tolerances than other models. Investigation revealed
that 62% of rework cases involved motherboard mounting misalignment causing
thermal sensor false positives during final test.

Contributing Factors:

1. COMPONENT FACTOR:
   Aluminum Chassis 16in from CasingCraft Manufacturing showed dimensional
   variance of +/- 0.3mm on mounting holes (spec: +/- 0.1mm). CasingCraft
   has 32 total rejected units during this period with a 3.3% rejection rate.

2. ASSEMBLY PROCESS FACTOR:
   The WorkStation 16 assembly jig was last calibrated in May 2025.
   Recommended calibration interval is 60 days. Jig deflection of 0.15mm
   was measured, contributing to alignment issues.

3. TESTING FACTOR:
   Final test thermal threshold was set at 72C, which is appropriate for
   standard models but too aggressive for the WorkStation 16's higher TDP
   processor. 18 final test failures were recorded for the AirBook 13 and
   18 for the ProBook 15 during the same period.

FISHBONE DIAGRAM SUMMARY:
- Machine: Assembly jig out of calibration
- Material: Chassis dimensional variance from CasingCraft
- Method: Thermal test threshold not model-specific
- Manpower: Operator training gap on WorkStation 16 specifics
```

### Page 4 — Financial Impact

```
FINANCIAL IMPACT

Direct Costs:
- Rework labor (58 units x 1.5 hrs x $35/hr): $3,045
- Scrap write-off (5 units x $1,200 standard cost): $6,000
- Additional machine hours (58 units x 0.5 hrs): 29 hours
- Material waste from scrapped units: $2,800

Indirect Costs:
- Schedule delay impact on 12 Make-to-Order customer orders: $8,400
  (estimated customer credit notes and expedited shipping)
- Production capacity lost to rework: 87 machine hours
  (could have produced 29 additional units)
- Quality team investigation time: 120 person-hours

Total Estimated Cost of Deviation: $20,245

INVENTORY IMPACT:
The WorkStation 16 current inventory at Austin warehouse is 29 units
with a status of "Low". The book value is $46,800. With only 2 units
in QC hold, the available-to-promise quantity is 29 units.
Combined with the yield issues, there is a risk of stockout within
2 weeks if demand continues at current levels.
```

### Page 5 — Corrective Actions

```
CORRECTIVE ACTIONS

IMMEDIATE (Implemented):
[DONE] Recalibrated WorkStation 16 assembly jig on September 2, 2025
[DONE] Adjusted thermal test threshold to 78C for WorkStation 16 model
[DONE] Added incoming inspection step for chassis dimensional check

SHORT-TERM (In Progress):
[IN PROGRESS] CasingCraft Manufacturing corrective action request issued
  - Response due: September 25, 2025
  - Requirement: Tighten mounting hole tolerance to +/- 0.15mm
[IN PROGRESS] Create model-specific assembly work instructions for WRK16
[IN PROGRESS] Schedule operator refresher training (12 assemblers)

LONG-TERM (Planned):
[PLANNED] Implement automated optical alignment verification station
  - Capital request: $85,000
  - Expected installation: Q1 2026
  - Projected yield improvement: +4% first pass yield
[PLANNED] Establish calibration tracking system with automated alerts
[PLANNED] Evaluate alternative chassis supplier for dual-sourcing

EFFECTIVENESS VERIFICATION:
Target: First pass yield >= 95% by November 2025
Monitoring: Weekly yield tracking by model in Manufacturing dashboard
Escalation: If yield does not reach 93% by October 15, escalate to VP Ops

APPROVAL:
Manufacturing Manager: _______________  Date: ___________
Quality Manager: _______________       Date: ___________
Plant Director: _______________        Date: ___________
```

---

## DOCUMENT 3: Shipping Incident Investigation Report

**Filename:** `SIR-2025-Q3-Carriers.pdf`

### Page 1 — Cover

```
TECHNOVA ELECTRONICS INC.
SHIPPING INCIDENT INVESTIGATION REPORT

Period: Q3 2025 (July - September)
Scope: All carriers — outbound laptop shipments
Report ID: SIR-2025-Q3-001
Prepared by: Logistics Operations
Classification: INTERNAL USE ONLY
Date: October 12, 2025
```

### Page 2 — Executive Summary & Carrier Overview

```
EXECUTIVE SUMMARY

Outbound shipping performance in Q3 2025 fell below target levels across
all three carriers. Overall on-time delivery to customers was 85.4%
against a target of 95%. A total of 482 shipments were dispatched,
with 71 arriving after the customer-promised delivery date.

This report investigates the root causes of delivery failures by carrier,
route, and product category, and recommends corrective measures.

CARRIER PERFORMANCE SUMMARY

Carrier                  | Shipments | OTD %  | Avg Transit | Late Count
RapidDeliver Couriers    | 173       | 87.3%  | 1.5 days    | 22
AirExpress Logistics     | 155       | 85.2%  | 1.5 days    | 23
LogiShip Express         | 154       | 83.8%  | 1.5 days    | 25

IMPORTANT NOTE ON METRIC DEFINITION:
"On-time delivery" in this logistics report measures carrier performance:
actual delivery date vs customer-promised date. This is NOT the same as
Procurement's "supplier on-time delivery" which measures supplier goods
receipt vs supplier-promised date. Both use the term "OTD" but measure
different events at different points in the supply chain.

Similarly, "lead time" here means transit time (dispatch to doorstep),
averaging 1.5 days. Procurement measures PO-to-receipt (~11 days).
Sales measures order-to-delivery (~12 days end-to-end).
```

### Page 3 — Incident Analysis by Region

```
INCIDENT ANALYSIS BY DELIVERY COUNTRY

India (IN) — Domestic Deliveries:
- Highest volume destination
- OTD: 88.1%
- Common issue: Last-mile delivery delays in Bangalore and Mumbai
- Incidents: 4 cases of damaged packaging (humidity during monsoon)

United States (US):
- OTD: 84.2%
- Common issue: Customs clearance delays for international shipments
- Incidents: 2 cases of misrouted packages (Chicago hub)
- One shipment to QuantumLeap Ltd (Chicago) delayed 3 days

Germany (DE):
- OTD: 86.7%
- Common issue: EU customs documentation incomplete
- Incidents: 1 case of delivery to wrong address (Berlin)
- Thomas Andersen (Berlin) delivery was on-time but re-routed

United Kingdom (GB):
- OTD: 82.3%
- Common issue: Post-Brexit customs processing adds 1 day average
- Most affected carrier: LogiShip Express (handling majority of UK routes)

SPECIFIC NOTABLE INCIDENTS:

Incident SH-INC-001: Shipment SH00000006 to QuantumLeap Ltd (Chicago)
  Carrier: LogiShip Express | Route: RT0004
  Product: 4x TechNova EduBook 14 Laptop
  Dispatch: Feb 20 | Delivery: Feb 22 | Promised: Feb 19
  Delay: 3 days | Root cause: Weather delay at logistics hub
  Customer impact: Partial order cancellation threat

Incident SH-INC-002: Shipment SH00000001 to Ravi Kumar (Bangalore)
  Carrier: RapidDeliver Couriers | Route: RT0001
  Product: 1x TechNova ProBook 15 Laptop
  Dispatch: Jan 11 | Delivery: Jan 13 | Promised: Jan 10
  Delay: 3 days | Root cause: Warehouse dispatch delay (goods issue late)
  Customer impact: Complaint filed, credit note issued
```

### Page 4 — Root Cause Breakdown

```
ROOT CAUSE CATEGORIZATION (71 late shipments)

Category                        | Count | % of Late
Carrier transit delay           | 28    | 39%
Warehouse dispatch delay        | 18    | 25%
Customs/documentation           | 12    | 17%
Address/routing error           | 7     | 10%
Weather/force majeure           | 4     | 6%
Damaged in transit (reshipment) | 2     | 3%

KEY FINDING: 25% of late deliveries originated from warehouse dispatch
delays (goods issue date later than planned). This is NOT a carrier
problem — it is an internal warehouse operations issue.

The logistics team receives goods for shipment only after the warehouse
completes picking and goods issue. If warehouse operations are delayed
(due to stock unavailability, QC holds, or staffing), the carrier
pickup is pushed back, making the delivery appear late.

CROSS-DOMAIN DEPENDENCY:
Warehouse stock health directly impacts logistics performance.
Current warehouse status shows:
- TechNova AirBook 13: Low stock (43 units, 6 in QC hold)
- TechNova WorkStation 16: Low stock (29 units, 2 in QC hold)
Low stock items take longer to pick and pack, adding 0.5-1 day to dispatch.

CARRIER-SPECIFIC ISSUES:
LogiShip Express: Weakest customs documentation process for EU/UK routes.
  Recommendation: Pre-clearance documentation package for all EU shipments.
AirExpress Logistics: Hub congestion at peak periods.
  Recommendation: Priority lane agreement for TechNova shipments.
RapidDeliver Couriers: Best performing but inconsistent India last-mile.
  Recommendation: Local delivery partner for Tier-2 Indian cities.
```

### Page 5 — Recommendations & SLA Review

```
RECOMMENDATIONS

1. WAREHOUSE-LOGISTICS HANDOFF (Addresses 25% of delays):
   - Implement daily dispatch readiness review at 8:00 AM
   - Pre-stage orders for next-day shipment during afternoon shift
   - Alert logistics team when goods issue is delayed by >2 hours

2. CUSTOMS PRE-CLEARANCE (Addresses 17% of delays):
   - Pre-file customs documentation for UK and EU shipments 48 hours ahead
   - Assign dedicated customs broker for German and UK routes
   - Create standardized documentation templates per destination country

3. CARRIER SLA RENEGOTIATION:
   Current SLA: 95% OTD with 3-day transit for international
   Proposed: Tiered SLA by priority level
   - Priority 1 (Make-to-Order): 98% OTD, 2-day transit, penalty clause
   - Priority 2 (Standard): 95% OTD, 3-day transit
   - Priority 3 (Economy): 90% OTD, 5-day transit

4. CARRIER ALLOCATION REBALANCING:
   - Shift 15% of UK volume from LogiShip Express to AirExpress Logistics
   - Assign RapidDeliver Couriers as primary for all India domestic
   - Quarterly carrier scorecards published to all three carriers

FINANCIAL JUSTIFICATION:
Current cost of late deliveries (Q3): ~$32,000
- Customer credits: $18,000
- Expedited reshipments: $8,000
- Internal handling: $6,000
Investment in recommendations: ~$15,000/quarter
Expected improvement: OTD from 85.4% to 92%+ within 2 quarters

APPROVED BY:
Logistics Manager: _______________   Date: ___________
Warehouse Manager: _______________   Date: ___________
VP Operations: _______________       Date: ___________
```

---

## DOCUMENT 4: Quarterly Inventory Audit Memo

**Filename:** `INV-AUDIT-2025-Q3-Austin.pdf`

### Page 1 — Cover

```
TECHNOVA ELECTRONICS INC.
QUARTERLY INVENTORY AUDIT MEMORANDUM

Facility: Austin Finished Goods Warehouse
Audit Period: Q3 2025 (July - September)
Memo ID: INV-AUDIT-2025-Q3-001
Prepared by: Warehouse Operations & Finance
Classification: CONFIDENTIAL — FINANCE REVIEW
Date: October 8, 2025
```

### Page 2 — Audit Scope & Inventory Position

```
AUDIT SCOPE

This memorandum summarizes the Q3 2025 physical inventory audit conducted
at the Austin Finished Goods Warehouse. The audit covers all laptop
finished goods (FERT category) stored at Plant P400, Storage Location 0001.

The audit reconciles physical counts against system records (SAP inventory
snapshot), identifies discrepancies, and assesses inventory health for
financial reporting and operational planning purposes.

CURRENT INVENTORY POSITION (as of latest snapshot)

Product                          | Physical | QC Hold | ATP  | Status  | Book Value
TechNova EduBook 14 Laptop      | 69       | 3       | 69   | Healthy | $35,550
TechNova ProBook 14 Laptop      | 62       | 4       | 62   | Healthy | $48,960
TechNova ProBook 15 Laptop      | 59       | 7       | 59   | Healthy | $51,750
TechNova AirBook 13 Laptop      | 43       | 6       | 43   | Low     | $29,150
TechNova WorkStation 16 Laptop  | 29       | 2       | 29   | Low     | $46,800
TOTAL                            | 262      | 22      | 247  |         | $212,210

IMPORTANT METRIC DEFINITIONS:
Physical Stock = total units physically on shelves (includes QC hold)
QC Hold = units quarantined for quality inspection (cannot be shipped)
ATP (Available to Promise) = units committable to new customer orders
Book Value = Physical Stock x Standard Price per Unit

NOTE: Warehouse measures inventory in UNITS (physical count).
Finance measures inventory in DOLLARS (book value for balance sheet).
Planning measures inventory in DAYS (days of inventory = stock / daily demand).
All three perspectives describe the same physical stock but serve different
business purposes. This is a key principle of the governed ontology.
```

### Page 3 — Audit Findings

```
AUDIT FINDINGS

FINDING 1: SLOW-MOVING INVENTORY — AirBook 13
Current stock: 43 units | Status: Low
Days of inventory (Planning metric): 3 days
Issue: Despite being classified as "Low" stock, the AirBook 13 has the
lowest demand forecast accuracy (per Planning persona data). Production
has generated 1,361 good units this period with a 99.6% first pass yield,
yet warehouse stock remains low due to high customer demand.
Recommendation: Increase production plan allocation for AirBook 13 by 15%.

FINDING 2: QC HOLD CONCENTRATION — ProBook 15
Current QC Hold: 7 units (highest across all products)
Issue: 7 units of ProBook 15 are held for quality inspection, representing
11.9% of its physical stock. Quality notifications indicate ProBook 15
had 18 final test failures during the period with an average rejection
rate of 8.9%. These held units reduce effective ATP.
Recommendation: Expedite QC clearance; coordinate with Quality team
to resolve outstanding notifications within 5 business days.

FINDING 3: STOCKOUT RISK — WorkStation 16
Current stock: 29 units | Status: Low | Book Value: $46,800
Issue: The WorkStation 16 has the lowest stock quantity and highest unit
value ($1,200 standard cost). With manufacturing yield issues (90.2%
first pass yield — lowest across all models), replenishment is constrained.
The low stock combined with production deviations (see PDR-2025-08-001)
creates a stockout risk within 10-14 days at current demand rates.
Recommendation: Expedite 2 production batches; consider temporary
allocation hold for non-priority customer orders.

FINDING 4: CYCLE COUNT DISCREPANCY
During physical count, 3 units of EduBook 14 were found in incorrect
storage bin (Bin A-14 instead of Bin B-22). System records were accurate
but physical placement was wrong. No financial impact but potential for
mis-picks during order fulfillment.
Recommendation: Warehouse team to conduct bin verification sweep.
```

### Page 4 — Financial Analysis

```
FINANCIAL ANALYSIS

INVENTORY VALUATION SUMMARY
Total Book Value: $212,210
Valuation Method: Standard Cost
Standard costs last updated: Q2 2025

Standard Cost per Unit:
- ProBook 15: $750 (highest margin product)
- ProBook 14: $680
- AirBook 13: $550 (best-selling model)
- EduBook 14: $450 (education segment)
- WorkStation 16: $1,200 (premium workstation)

INVENTORY TURNS ANALYSIS
Warehouse perspective (physical movement based):
- Average turns across laptops: 9.0 - 10.0x annually
- Highest: EduBook 14 at 10.0x (high volume, fast moving)
- Lowest: AirBook 13 at 9.0x

Finance perspective (book-value based, typically lower):
- Average turns: 6.0 - 7.5x annually
- The difference is because Finance uses landed cost basis while
  Warehouse uses physical movement. Both are correct for their
  respective purposes — this is a key ontology disambiguation.

WRITE-OFF & PROVISION RECOMMENDATIONS
- No obsolescence write-off required (all products currently selling)
- Provision for QC hold units: $15,400 (22 units at weighted avg cost)
  These may be released or scrapped pending Quality team resolution.
- Slow-moving provision: None required (all products within 30-day turns)

LANDED COST vs STANDARD COST NOTE:
Finance calculates landed cost = materials + labor + freight + duty.
For a ProBook 15 battery laptop:
  Procurement cost (PO price): $400
  Manufacturing cost (materials + labor): $450
  Landed cost (Finance view): $480 (adds $20 freight + $10 duty)
  Standard cost (Warehouse valuation): $750 (includes overhead allocation)
The standard cost used for inventory valuation is HIGHER than landed cost
because it includes manufacturing overhead and margin allocation.
```

### Page 5 — Recommendations & Sign-Off

```
RECOMMENDATIONS

1. REPLENISHMENT PRIORITIES:
   - URGENT: WorkStation 16 — trigger 2 production batches of 20 units each
   - HIGH: AirBook 13 — increase monthly production plan by 15%
   - MONITOR: ProBook 15 — resolve QC hold before requesting production

2. QC HOLD RESOLUTION:
   - 22 units currently in QC hold across all products (value: $15,400)
   - Coordinate with Quality Manager to disposition within 10 business days
   - If units are scrapped, Finance to process write-off in October close

3. WAREHOUSE OPERATIONS:
   - Complete bin verification sweep by October 15
   - Implement barcode scan verification at put-away step
   - Review picking sequence to reduce mis-picks

4. INVENTORY POLICY REVIEW:
   - Current safety stock levels may be insufficient for premium models
   - Propose increasing WorkStation 16 safety stock from 25 to 40 units
   - Propose increasing AirBook 13 safety stock from 40 to 55 units

5. CROSS-FUNCTIONAL ALIGNMENT:
   - Share this memo with Planning Manager for production adjustment
   - Share QC hold details with Quality Manager
   - Share financial impact with Finance Manager for Q3 close

NEXT AUDIT: January 2026 (Q4 2025 audit)

APPROVED:
Warehouse Manager: _______________    Date: ___________
Finance Controller: _______________   Date: ___________
VP Supply Chain: _______________      Date: ___________
```

---

## DOCUMENT 5: Supplier Contract Summary — ChipWorks Semiconductor

**Filename:** `CONTRACT-2025-ChipWorks-Semiconductor.pdf`

### Page 1 — Cover

```
TECHNOVA ELECTRONICS INC.
SUPPLIER CONTRACT SUMMARY

Supplier: ChipWorks Semiconductor
Location: Hsinchu, Taiwan
Contract Period: January 1, 2025 — December 31, 2025
Contract ID: SC-2025-CHIP-001
Prepared by: Procurement & Legal
Classification: CONFIDENTIAL — AUTHORIZED PERSONNEL ONLY
Date: January 15, 2025
```

### Page 2 — Contract Overview & Terms

```
CONTRACT OVERVIEW

ChipWorks Semiconductor is a Tier 1 strategic supplier providing
processor and semiconductor components for all TechNova laptop models.
This contract governs the supply of the following components:

Components Under Contract:
- Intel Core i7 Processor 13th Gen (RM-PROC-I7)
- Intel Core i5 Processor 13th Gen (RM-PROC-I5)
- Li-Ion Battery Cell 56Wh (RM-BAT-56WH) — secondary source

Current Performance (YTD):
- On-Time Delivery: 94.3% (meets target)
- Incoming Rejection Rate: 0.7% (meets target)
- Average Lead Time: 11.1 days
- Total PO Lines: 35
- Risk Classification: GREEN

CONTRACT TERMS

Term: 12 months (auto-renewal with 90-day notice)
Minimum Order Quantity: 50 units per PO line
Payment Terms: Net 45 days from goods receipt
Currency: USD
Incoterms: DDP Austin, TX (Delivered Duty Paid)
Insurance: Supplier responsibility until warehouse receipt
```

### Page 3 — Pricing & Volume Commitments

```
PRICING SCHEDULE

Component                       | Tier 1 (0-500) | Tier 2 (501-1000) | Tier 3 (1001+)
Intel Core i7 Processor 13th Gen| $280/unit       | $265/unit          | $250/unit
Intel Core i5 Processor 13th Gen| $195/unit       | $185/unit          | $175/unit
Li-Ion Battery Cell 56Wh        | $355/unit       | $340/unit          | $325/unit

Annual Volume Commitment: Minimum 3,000 units across all components
Volume Rebate: 2% rebate on total annual spend if commitment met
Price Adjustment: Annual review, maximum increase 5% with 60-day notice

PROCUREMENT COST NOTE:
These prices represent the PROCUREMENT view of cost (PO unit price only).
They do NOT include:
- Labor cost ($50/unit added during Manufacturing assembly)
- Freight cost ($20/unit added by Logistics)
- Import duty ($10/unit added at customs)
The FINANCE view (landed cost) is therefore $60-80 higher per unit
than these contract prices. This distinction is critical for accurate
cost reporting across personas.

ESTIMATED ANNUAL SPEND

Based on 2025 demand forecast:
- i7 Processors: 1,200 units x $265 avg = $318,000
- i5 Processors: 1,500 units x $185 avg = $277,500
- Battery 56Wh: 500 units x $340 avg = $170,000 (secondary source)
Total estimated: $765,500
```

### Page 4 — Service Level Agreements

```
SERVICE LEVEL AGREEMENTS (SLAs)

1. DELIVERY PERFORMANCE
   Target: >= 95% on-time delivery (measured at goods receipt)
   Measurement: Monthly, based on supplier_promised_date vs gr_date
   Current Performance: 94.3% (marginal — within 1% of target)
   Penalty: 1% of affected PO value for each percentage point below 90%
   Bonus: 0.5% discount on next quarter if OTD exceeds 98%

2. QUALITY PERFORMANCE
   Target: < 2% incoming inspection rejection rate
   Measurement: Monthly, based on incoming_rejected_qty / order_quantity
   Current Performance: 0.7% (excellent)
   Penalty: Full replacement at supplier cost for rejected units
   Escalation: If rejection exceeds 5% for 2 consecutive months,
   TechNova reserves right to audit supplier facility

3. LEAD TIME
   Committed Lead Time: 10 business days from PO date to goods receipt
   Current Average: 11.1 days (slightly above commitment)
   Emergency Orders: 5 business days at 15% premium
   Note: This lead time is the PROCUREMENT definition (PO-to-receipt).
   Customer-facing lead time (SALES definition) is ~12 days total.

4. DOCUMENTATION
   Three-Way Match: PO qty = GR qty = Invoice qty required for payment
   Invoice submission: Within 5 days of goods receipt
   Certificate of Compliance: Required with each shipment

5. BUSINESS CONTINUITY
   Safety stock at ChipWorks: Minimum 2 weeks of TechNova demand
   Disaster recovery: Alternative production site within 30 days
   Force majeure: Notification within 24 hours; mitigation plan in 72 hours
```

### Page 5 — Risk Assessment & Governance

```
RISK ASSESSMENT

GEOPOLITICAL RISK: MEDIUM
Taiwan semiconductor industry faces ongoing geopolitical tensions.
Mitigation: Evaluate secondary processor source from South Korean suppliers.
ChipWorks has committed to maintaining 4-week buffer inventory.

SINGLE-SOURCE RISK: HIGH (for i7 processor)
ChipWorks is the sole supplier for Intel Core i7 13th Gen processors.
Mitigation: Qualify BoardMaster PCB (China) as secondary source by Q2 2026.
Until dual-sourced, maintain 6-week safety stock for i7 processors.

CURRENCY RISK: LOW
Contract is USD-denominated. No forex exposure.

QUALITY RISK: LOW
0.7% rejection rate is well within the 2% threshold.
ChipWorks has ISO 9001:2015 and IATF 16949 certifications.

SUPPLY CHAIN POSITION IN ONTOLOGY:
ChipWorks sits at the SUPPLIER -> COMPONENT stage of the supply chain.
Their output feeds into:
  Procurement (PO management) ->
    Quality Incoming Inspection ->
      Manufacturing Assembly ->
        Final Test ->
          Warehouse ->
            Sales Order Fulfillment ->
              Logistics Delivery ->
                Customer
A disruption at ChipWorks propagates through ALL downstream stages.

CONTRACT GOVERNANCE

Quarterly Business Reviews: January, April, July, October
Annual Contract Review: November (for next-year renewal)
Primary Contact at ChipWorks: James Chen, VP Sales
TechNova Contract Owner: Procurement Manager
Escalation Path: Procurement -> VP Supply Chain -> CEO (within 48 hours)

SIGNATURES:
TechNova Procurement Director: _______________  Date: ___________
ChipWorks VP Sales: _______________            Date: ___________
TechNova Legal Counsel: _______________        Date: ___________
```
