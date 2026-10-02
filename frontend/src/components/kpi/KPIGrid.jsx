import './KPIGrid.css';

export default function KPIGrid({ kpis }) {
  if (!kpis || kpis.length === 0) return null;

  return (
    <div className="kpi-section">
      <h3 className="section-title">Key Performance Indicators</h3>
      <div className="kpi-grid">
        {kpis.map((kpi) => (
          <div key={kpi.id} className="kpi-card">
            <div className="kpi-name">{kpi.name}</div>
            <div className="kpi-value">
              {kpi.value}
              {kpi.unit && <span className="kpi-unit">{kpi.unit}</span>}
            </div>
            <div className="kpi-desc">{kpi.description}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
