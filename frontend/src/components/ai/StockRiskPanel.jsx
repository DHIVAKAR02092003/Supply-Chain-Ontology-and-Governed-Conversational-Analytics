import { useState } from 'react';
import { ShieldAlert, Package, AlertTriangle, CheckCircle, TrendingDown, Loader2 } from 'lucide-react';
import { getStockRisk } from '../../api/client';
import './StockRiskPanel.css';
import './ai-shared.css';

const RISK_CONFIG = {
  'Critical - Reorder Now': { icon: AlertTriangle, className: 'risk-critical' },
  'Low Stock - Monitor': { icon: TrendingDown, className: 'risk-low' },
  'Healthy': { icon: CheckCircle, className: 'risk-healthy' },
  'Overstocked': { icon: Package, className: 'risk-overstock' },
};

export default function StockRiskPanel() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleGenerate = () => {
    setLoading(true);
    setError(null);
    getStockRisk()
      .then(setData)
      .catch(e => setError(e.message))
      .finally(() => setLoading(false));
  };

  return (
    <div className="stock-risk-section">
      <div className="ai-panel-header">
        <h3 className="section-title">
          <ShieldAlert size={16} /> AI Stock Risk Classification
          <span className="ai-badge">AI_CLASSIFY</span>
        </h3>
        <button className="ai-generate-btn" onClick={handleGenerate} disabled={loading}>
          {loading ? <><Loader2 size={14} className="spinning" /> Classifying...</> : data ? 'Regenerate' : 'Generate Classification'}
        </button>
      </div>

      {error && <div className="ai-error">Failed to classify stock risk. Please try again.</div>}

      {data && data.length > 0 && (
        <div className="stock-risk-grid">
          {data.map((item, i) => {
            const config = RISK_CONFIG[item.risk_label] || RISK_CONFIG['Healthy'];
            const Icon = config.icon;
            return (
              <div key={i} className={`stock-risk-card ${config.className}`}>
                <div className="risk-card-header">
                  <Icon size={16} />
                  <span className="risk-label">{item.risk_label}</span>
                </div>
                <div className="risk-product">{item.product}</div>
                <div className="risk-details">
                  <span>Stock: {item.stock_qty?.toLocaleString()} units</span>
                  <span>Utilization: {item.utilization_pct}%</span>
                  <span>ATP: {item.atp?.toLocaleString()}</span>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
