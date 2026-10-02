import {
  ShoppingCart, Factory, Warehouse as WarehouseIcon,
  TrendingUp, Truck, Calendar, Shield, DollarSign,
  Network, MessageSquareText
} from 'lucide-react';
import './PersonaNav.css';

const iconMap = {
  ShoppingCart, Factory, Warehouse: WarehouseIcon,
  TrendingUp, Truck, Calendar, Shield, DollarSign
};

export default function PersonaNav({ personas, activePersona, onSelect }) {
  return (
    <nav className="persona-nav">
      <div className="nav-label">Personas</div>
      
      {/* 1st Tab: Ontology */}
      <button
        className={`persona-item ${activePersona === 'architecture' ? 'active' : ''}`}
        onClick={() => onSelect('architecture')}
      >
        <Network size={18} className="persona-icon" />
        <div className="persona-info">
          <span className="persona-name">Ontology</span>
          <span className="persona-desc">Live Supply Chain Ontology</span>
        </div>
      </button>

      {personas.map((p) => {
        const Icon = iconMap[p.icon] || ShoppingCart;
        return (
          <button
            key={p.id}
            className={`persona-item ${activePersona === p.id ? 'active' : ''}`}
            onClick={() => onSelect(p.id)}
          >
            <Icon size={18} className="persona-icon" />
            <div className="persona-info">
              <span className="persona-name">{p.name}</span>
              <span className="persona-desc">{p.description?.slice(0, 50)}...</span>
            </div>
          </button>
        );
      })}

      {/* 10th Tab: Speak with Data */}
      <button
        className={`persona-item ${activePersona === 'speak_with_data' ? 'active' : ''}`}
        onClick={() => onSelect('speak_with_data')}
      >
        <MessageSquareText size={18} className="persona-icon" />
        <div className="persona-info">
          <span className="persona-name">Speak with Data</span>
          <span className="persona-desc">Conversational Agent UI</span>
        </div>
      </button>
    </nav>
  );
}
