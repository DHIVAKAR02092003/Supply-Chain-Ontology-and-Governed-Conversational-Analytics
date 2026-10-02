import { GitBranch } from 'lucide-react';
import './OntologyRelationships.css';

export default function OntologyRelationships({ persona, ontology }) {
  return (
    <div className="ontology-rel-section">
      <h3 className="section-title">Cross-Persona Impact</h3>
      <div className="ontology-rel-card">
        <div className="impact-flow">
          <GitBranch size={16} className="impact-icon" />
          <p className="impact-text">{ontology.cross_impact}</p>
        </div>

        <div className="rel-grid">
          <div className="rel-col">
            <h4>Upstream Dependencies</h4>
            <p className="rel-desc">Who provides information or materials to {persona.name}?</p>
            <div className="rel-items">
              {ontology.upstream.map(u => (
                <div key={u} className="rel-item upstream">{u}</div>
              ))}
            </div>
          </div>
          <div className="rel-col">
            <h4>Downstream Impact</h4>
            <p className="rel-desc">Who depends on {persona.name}?</p>
            <div className="rel-items">
              {ontology.downstream.map(d => (
                <div key={d} className="rel-item downstream">{d}</div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
