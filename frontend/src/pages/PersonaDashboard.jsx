import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Layers, Home } from 'lucide-react';
import { getPersonas } from '../api/client';
import { usePersonaData } from '../hooks/usePersonaData';
import PersonaNav from '../components/persona/PersonaNav';
import PersonaHeader from '../components/persona/PersonaHeader';
import KPIGrid from '../components/kpi/KPIGrid';
import ChartGrid from '../components/charts/ChartGrid';
import InsightsPanel from '../components/persona/InsightsPanel';
import OntologyRelationships from '../components/persona/OntologyRelationships';
import LoadingSkeleton from '../components/common/LoadingSkeleton';
import ThemeToggle from '../components/common/ThemeToggle';
import SupplyChainFlow from '../components/ontology/SupplyChainFlow';
import AgentUI from '../components/persona/AgentUI';
import StockRiskPanel from '../components/ai/StockRiskPanel';
import QualitySentimentPanel from '../components/ai/QualitySentimentPanel';
import './PersonaDashboard.css';

export default function PersonaDashboard() {
  const navigate = useNavigate();
  const [personas, setPersonas] = useState([]);
  const [activePersona, setActivePersona] = useState(null);
  const { data, loading, error } = usePersonaData(activePersona);

  useEffect(() => {
    getPersonas().then((list) => {
      setPersonas(list);
      if (!activePersona) setActivePersona('architecture');
    });
  }, []);

  return (
    <div className="dashboard-layout">
      <header className="dash-header">
        <div className="dash-header-left">
          <Layers size={20} className="dash-logo-icon" />
          <span className="dash-title">SupplyChain Intelligence</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center' }}>
          <ThemeToggle />
          <button className="back-btn" onClick={() => navigate('/')}>
            <Home size={16} /> Home
          </button>
        </div>
      </header>

      <div className="dash-body">
        <PersonaNav
          personas={personas}
          activePersona={activePersona}
          onSelect={setActivePersona}
        />

        <main className="dash-main">
          {activePersona === 'architecture' && <SupplyChainFlow />}
          {activePersona === 'speak_with_data' && <AgentUI />}
          
          {activePersona !== 'architecture' && activePersona !== 'speak_with_data' && (
            <>
              {loading && <LoadingSkeleton />}
              {error && <div className="error-state">Error loading data: {error}</div>}
              {!loading && !error && data && (
                <>
                  <PersonaHeader persona={data.persona} ontology={data.ontology} />
                  <KPIGrid kpis={data.kpis} />
                  <ChartGrid charts={data.charts} />
                  <InsightsPanel insights={data.insights} personaId={activePersona} />
                  {activePersona === 'warehouse' && <StockRiskPanel />}
                  {activePersona === 'quality' && <QualitySentimentPanel />}
                  <OntologyRelationships persona={data.persona} ontology={data.ontology} />
                </>
              )}
            </>
          )}
        </main>
      </div>
    </div>
  );
}
