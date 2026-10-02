import './LoadingSkeleton.css';

export default function LoadingSkeleton() {
  return (
    <div className="skeleton-container">
      <div className="skeleton-header">
        <div className="skel skel-title" />
        <div className="skel skel-subtitle" />
      </div>
      <div className="skeleton-kpis">
        {[...Array(8)].map((_, i) => (
          <div key={i} className="skel skel-kpi" />
        ))}
      </div>
      <div className="skeleton-charts">
        <div className="skel skel-chart" />
        <div className="skel skel-chart" />
      </div>
    </div>
  );
}
