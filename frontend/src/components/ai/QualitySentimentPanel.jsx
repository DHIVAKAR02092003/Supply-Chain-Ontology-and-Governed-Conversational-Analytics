import { useState } from 'react';
import { Activity, TrendingDown, TrendingUp, Minus, Loader2 } from 'lucide-react';
import { getQualitySentiment } from '../../api/client';
import './QualitySentimentPanel.css';
import './ai-shared.css';

function getSentimentInfo(score) {
  if (score <= -0.3) return { label: 'Negative', icon: TrendingDown, className: 'sentiment-negative' };
  if (score >= 0.3) return { label: 'Positive', icon: TrendingUp, className: 'sentiment-positive' };
  return { label: 'Neutral', icon: Minus, className: 'sentiment-neutral' };
}

export default function QualitySentimentPanel() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleGenerate = () => {
    setLoading(true);
    setError(null);
    getQualitySentiment()
      .then(setData)
      .catch(e => setError(e.message))
      .finally(() => setLoading(false));
  };

  return (
    <div className="sentiment-section">
      <div className="ai-panel-header">
        <h3 className="section-title">
          <Activity size={16} /> AI Quality Sentiment Analysis
          <span className="ai-badge">AI_SENTIMENT</span>
        </h3>
        <button className="ai-generate-btn" onClick={handleGenerate} disabled={loading}>
          {loading ? <><Loader2 size={14} className="spinning" /> Analyzing...</> : data ? 'Regenerate' : 'Analyze Sentiment'}
        </button>
      </div>

      {error && <div className="ai-error">Failed to analyze sentiment. Please try again.</div>}

      {data && data.length > 0 && (
        <div className="sentiment-table-wrapper">
          <table className="sentiment-table">
            <thead>
              <tr>
                <th>Material</th>
                <th>Supplier</th>
                <th>Type</th>
                <th>Rejected</th>
                <th>Rate %</th>
                <th>Sentiment</th>
              </tr>
            </thead>
            <tbody>
              {data.map((item, i) => {
                const info = getSentimentInfo(item.sentiment);
                const Icon = info.icon;
                return (
                  <tr key={i}>
                    <td className="cell-material">{item.material}</td>
                    <td>{item.supplier || 'N/A'}</td>
                    <td>{item.inspection_type}</td>
                    <td>{item.rejected_qty}</td>
                    <td>{item.rejection_rate}%</td>
                    <td>
                      <span className={`sentiment-badge ${info.className}`}>
                        <Icon size={12} />
                        {item.sentiment?.toFixed(2)} ({info.label})
                      </span>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
