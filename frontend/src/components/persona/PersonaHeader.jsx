import './PersonaHeader.css';

export default function PersonaHeader({ persona, ontology }) {
  return (
    <div className="persona-header">
      <div className="ph-top">
        <div>
          <h1 className="ph-name">{persona.name}</h1>
          <p className="ph-desc">{persona.description}</p>
        </div>
        <div className="ph-entity-badge">{persona.entity}</div>
      </div>

      <div className="ph-why">
        <h3>Why This Persona Matters</h3>
        <p>{persona.why_matters}</p>
      </div>

      <div className="ph-position">
        <div className="ph-deps">
          <span className="dep-label">Upstream</span>
          <div className="dep-tags">
            {ontology.upstream.map(u => <span key={u} className="dep-tag upstream">{u}</span>)}
          </div>
        </div>
        <div className="ph-arrow">→</div>
        <div className="ph-current">
          <span className="current-badge">{persona.name}</span>
        </div>
        <div className="ph-arrow">→</div>
        <div className="ph-deps">
          <span className="dep-label">Downstream</span>
          <div className="dep-tags">
            {ontology.downstream.map(d => <span key={d} className="dep-tag downstream">{d}</span>)}
          </div>
        </div>
      </div>
    </div>
  );
}
