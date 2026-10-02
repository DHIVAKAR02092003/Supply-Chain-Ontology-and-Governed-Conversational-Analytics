import { useState } from 'react';
import { 
  FileText, Package, CheckCircle, LineChart, 
  Settings, Factory, ShieldCheck, ShoppingCart, 
  TrendingUp, ClipboardList, Truck, Receipt, User, X, Maximize, Minimize
} from 'lucide-react';
import './SupplyChainFlow.css';

const DOMAINS = [
  'Full Chain', 'Procurement', 'Quality', 'Planning', 'Warehouse', 
  'Manufacturing', 'Sales', 'Logistics', 'Finance'
];

const DOMAIN_COLORS = {
  'Procurement': { bg: '#fff7ed', border: '#fdba74', text: '#ea580c' },
  'Quality': { bg: '#fef2f2', border: '#fca5a5', text: '#dc2626' },
  'Planning': { bg: '#f5f3ff', border: '#c4b5fd', text: '#7c3aed' },
  'Warehouse': { bg: '#fefce8', border: '#fde047', text: '#ca8a04' },
  'Manufacturing': { bg: '#faf5ff', border: '#d8b4fe', text: '#9333ea' },
  'Sales': { bg: '#eff6ff', border: '#93c5fd', text: '#2563eb' },
  'Logistics': { bg: '#ecfeff', border: '#67e8f9', text: '#0891b2' },
  'Finance': { bg: '#f0fdf4', border: '#86efac', text: '#16a34a' },
};

const NODE_DESCRIPTIONS = {
  'supplier': 'External vendors providing raw materials and components.',
  'po': 'Purchase Orders issued to suppliers for procurement of goods.',
  'qa_in': 'Incoming Quality Assurance inspections for received materials.',
  'invoice': 'Financial ledgers and invoices tracking payables and receivables.',
  'mrp': 'Material Requirements Planning execution to determine material needs.',
  'material': 'Raw materials and components stored in the warehouse.',
  'bom': 'Bill of Materials defining the components needed for manufacturing.',
  'fg': 'Finished Goods ready for sale and distribution.',
  'prod_order': 'Production Orders triggering the manufacturing of finished goods.',
  'forecast': 'Demand Forecast predicting future sales to drive planning.',
  'qa_out': 'Final Quality Assurance testing for finished goods before shipment.',
  'sales_order': 'Sales Orders placed by customers for finished goods.',
  'delivery': 'Delivery processing grouping sales orders for logistics.',
  'customer': 'End customers purchasing the finished goods.',
  'shipment': 'Outbound shipments moving goods to the customer.'
};

const NODES = [
  { id: 'supplier', label: 'SUPPLIER', domain: 'Procurement', x: 30, y: 220, stats: '12 vendors' },
  { id: 'po', label: 'PURCHASE ORDER', domain: 'Procurement', x: 30, y: 380, stats: '35 open POs' },
  { id: 'qa_in', label: 'INCOMING QA', domain: 'Quality', x: 210, y: 220, stats: '5 pending' },
  { id: 'invoice', label: 'INVOICE / LEDGER', domain: 'Finance', x: 570, y: 520, stats: '$1.2M pending' },
  { id: 'mrp', label: 'MRP RUN', domain: 'Planning', x: 210, y: 60, stats: 'Daily' },
  { id: 'material', label: 'MATERIAL', domain: 'Warehouse', x: 390, y: 220, stats: '120 items' },
  { id: 'bom', label: 'BOM', domain: 'Manufacturing', x: 570, y: 60, stats: '4 active' },
  { id: 'fg', label: 'FINISHED GOOD', domain: 'Warehouse', x: 570, y: 220, stats: '8 products' },
  { id: 'prod_order', label: 'PRODUCTION ORDER', domain: 'Manufacturing', x: 570, y: 380, stats: '15 active' },
  { id: 'forecast', label: 'DEMAND FORECAST', domain: 'Planning', x: 750, y: 60, stats: 'Monthly' },
  { id: 'qa_out', label: 'FINAL QA', domain: 'Quality', x: 750, y: 220, stats: '2 in test' },
  { id: 'sales_order', label: 'SALES ORDER', domain: 'Sales', x: 930, y: 220, stats: '45 orders' },
  { id: 'delivery', label: 'DELIVERY', domain: 'Logistics', x: 750, y: 380, stats: '12 outbound' },
  { id: 'customer', label: 'CUSTOMER', domain: 'Sales', x: 1110, y: 220, stats: '8 accounts' },
  { id: 'shipment', label: 'SHIPMENT', domain: 'Logistics', x: 930, y: 380, stats: '6 in transit' },
];

const EDGES = [
  { source: 'po', target: 'supplier', label: 'ISSUED TO', icon: FileText, duration: 3 },
  { source: 'supplier', target: 'qa_in', label: 'SUPPLIES', icon: Package, duration: 4 },
  { source: 'qa_in', target: 'material', label: 'INSPECTED', icon: ShieldCheck, duration: 3 },
  { source: 'forecast', target: 'mrp', label: 'DRIVES', icon: LineChart, duration: 4 },
  { source: 'mrp', target: 'po', label: 'GENERATES', icon: FileText, duration: 3 },
  { source: 'bom', target: 'material', label: 'CONSUMES', icon: Settings, duration: 3 },
  { source: 'bom', target: 'fg', label: 'PRODUCES', icon: Factory, duration: 3 },
  { source: 'prod_order', target: 'fg', label: 'MANUFACTURES', icon: Package, duration: 4 },
  { source: 'prod_order', target: 'material', label: 'RESERVES', icon: CheckCircle, duration: 3 },
  { source: 'fg', target: 'qa_out', label: 'TESTED BY', icon: ShieldCheck, duration: 3 },
  { source: 'qa_out', target: 'sales_order', label: 'FULFILLS', icon: CheckCircle, duration: 3 },
  { source: 'customer', target: 'sales_order', label: 'ORDERS', icon: User, duration: 4 },
  { source: 'customer', target: 'forecast', label: 'SIGNALS', icon: TrendingUp, duration: 5 },
  { source: 'sales_order', target: 'delivery', label: 'SHIPPED VIA', icon: ClipboardList, duration: 3 },
  { source: 'delivery', target: 'shipment', label: 'PACKED INTO', icon: Package, duration: 3 },
  { source: 'shipment', target: 'customer', label: 'DELIVERED TO', icon: Truck, duration: 4 },
  { source: 'po', target: 'invoice', label: 'BILLED', icon: Receipt, duration: 5 },
  { source: 'sales_order', target: 'invoice', label: 'REVENUE', icon: Receipt, duration: 4 },
];

export default function SupplyChainFlow() {
  const [activeTab, setActiveTab] = useState('Full Chain');
  const [selectedNode, setSelectedNode] = useState(null);
  const [isExpanded, setIsExpanded] = useState(false);

  const getEdgePath = (sourceNode, targetNode) => {
    const x1 = sourceNode.x + 80;
    const y1 = sourceNode.y + 42.5;
    const x2 = targetNode.x + 80;
    const y2 = targetNode.y + 42.5;
    
    const dx = x2 - x1;
    const dy = y2 - y1;
    
    if (Math.abs(dx) > Math.abs(dy)) {
      return `M ${x1} ${y1} C ${x1 + dx/3} ${y1}, ${x2 - dx/3} ${y2}, ${x2} ${y2}`;
    } else {
      return `M ${x1} ${y1} C ${x1} ${y1 + dy/3}, ${x2} ${y2 - dy/3}, ${x2} ${y2}`;
    }
  };

  const isNodeActive = (node) => activeTab === 'Full Chain' || node.domain === activeTab;
  
  const isEdgeActive = (edge) => {
    if (activeTab === 'Full Chain') return true;
    const sourceNode = NODES.find(n => n.id === edge.source);
    const targetNode = NODES.find(n => n.id === edge.target);
    return sourceNode?.domain === activeTab || targetNode?.domain === activeTab;
  };

  const handleNodeClick = (node) => {
    setSelectedNode(node);
  };

  return (
    <div className={`topology-container ${isExpanded ? 'expanded' : ''}`}>
      <div className="topology-header">
        <div className="topology-status">
          <div className="live-dot" />
          Live Persona Ontology
        </div>
        <div className="topology-stats" style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          <span>{NODES.length} nodes · {EDGES.length} edges · {DOMAINS.length - 1} personas</span>
          <button className="expand-btn" onClick={() => setIsExpanded(!isExpanded)} title={isExpanded ? "Collapse" : "Expand Fullscreen"}>
            {isExpanded ? <Minimize size={16} /> : <Maximize size={16} />}
          </button>
        </div>
      </div>

      <div className="topology-tabs">
        {DOMAINS.map(domain => (
          <button
            key={domain}
            className={`topology-tab ${activeTab === domain ? 'active' : ''}`}
            onClick={() => setActiveTab(domain)}
          >
            {domain}
          </button>
        ))}
      </div>

      <div className="topology-scroll-wrapper" style={{ overflowX: 'auto', width: '100%' }}>
        <div className="topology-canvas" style={{ minWidth: '1300px', height: '650px' }}>
          <svg className="topology-svg" viewBox="0 0 1300 650" preserveAspectRatio="xMidYMid meet">
            <defs>
              <marker id="arrow-inactive" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                <path d="M 0 0 L 10 5 L 0 10 z" fill="#cbd5e1" />
              </marker>
              <marker id="arrow-active" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                <path d="M 0 0 L 10 5 L 0 10 z" fill="#3b82f6" />
              </marker>
            </defs>

            {EDGES.map((edge, i) => {
              const sourceNode = NODES.find(n => n.id === edge.source);
              const targetNode = NODES.find(n => n.id === edge.target);
              if (!sourceNode || !targetNode) return null;

              const active = isEdgeActive(edge);
              const pathData = getEdgePath(sourceNode, targetNode);
              const midX = (sourceNode.x + targetNode.x) / 2 + 80;
              const midY = (sourceNode.y + targetNode.y) / 2 + 42.5;
              const labelWidth = edge.label.length * 6 + 12;
              const IconComponent = edge.icon;

              return (
                <g key={i}>
                  <path
                    id={`edge-path-${i}`}
                    d={pathData}
                    className={`edge-path ${active ? 'active' : 'inactive'}`}
                    markerMid={active ? 'url(#arrow-active)' : 'url(#arrow-inactive)'}
                  />
                  
                  {/* Moving Icon along the path */}
                  {active && (
                    <g className="moving-icon-group">
                      <g transform="translate(-12, -12)">
                        <IconComponent 
                          size={24} 
                          color={active ? '#3b82f6' : '#cbd5e1'} 
                          strokeWidth={active ? 2.5 : 1.5} 
                        />
                      </g>
                      <animateMotion dur={`${edge.duration}s`} repeatCount="indefinite">
                        <mpath href={`#edge-path-${i}`} />
                      </animateMotion>
                    </g>
                  )}

                  <g className={`edge-label-group ${active ? 'active' : 'inactive'}`} transform={`translate(${midX}, ${midY})`}>
                    <rect 
                      x={-labelWidth/2} y={-10} 
                      width={labelWidth} height={20} 
                      className="edge-label-bg" 
                    />
                    <text className="edge-label-text">{edge.label}</text>
                  </g>
                </g>
              );
            })}
          </svg>

          <div className="topology-nodes">
            {NODES.map(node => {
              const active = isNodeActive(node);
              const isSelected = selectedNode?.id === node.id;
              const colors = DOMAIN_COLORS[node.domain] || { bg: '#fff', border: '#e2e8f0', text: '#64748b' };
              
              return (
                <div
                  key={node.id}
                  className={`topology-node ${active ? 'active' : 'inactive'} ${isSelected ? 'selected' : ''}`}
                  style={{
                    left: node.x,
                    top: node.y,
                    borderColor: active || isSelected ? colors.border : '#e2e8f0',
                    boxShadow: isSelected ? `0 0 0 3px ${colors.border}40` : (active ? `0 0 0 1px ${colors.border}` : 'none')
                  }}
                  onClick={() => handleNodeClick(node)}
                >
                  <div 
                    className="node-domain"
                    style={{ color: active ? colors.text : '#94a3b8' }}
                  >
                    {node.domain}
                  </div>
                  <div className="node-label">{node.label}</div>
                  <div className="node-stats">{node.stats}</div>
                </div>
              );
            })}
          </div>
          
          {/* Entity Explanation Panel */}
          {selectedNode && (
            <div className="entity-panel">
              <div className="entity-panel-header">
                <div className="entity-panel-title">
                  <span className="entity-domain" style={{ color: DOMAIN_COLORS[selectedNode.domain]?.text }}>
                    {selectedNode.domain}
                  </span>
                  <h3>{selectedNode.label}</h3>
                </div>
                <button className="entity-panel-close" onClick={() => setSelectedNode(null)}>
                  <X size={18} />
                </button>
              </div>
              <div className="entity-panel-body">
                <p>{NODE_DESCRIPTIONS[selectedNode.id]}</p>
                <div className="entity-meta">
                  <strong>Current Stats:</strong> {selectedNode.stats}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
