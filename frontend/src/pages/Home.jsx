import { useNavigate } from 'react-router-dom';
import { ArrowRight, Link2, Layers, Users, Database } from 'lucide-react';
import ThemeToggle from '../components/common/ThemeToggle';
import './Home.css';

import AnimatedBackground from '../components/common/AnimatedBackground';

export default function Home() {
  const navigate = useNavigate();

  return (
    <div className="home">
      <AnimatedBackground />
      <header className="home-header">
        <div className="header-content">
          <div className="logo">
            <Layers size={24} />
            <span>SupplyChain Ontology</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center' }}>
            <ThemeToggle />
            <button className="nav-btn" onClick={() => navigate('/dashboard')}>
              Persona Dashboard <ArrowRight size={16} />
            </button>
          </div>
        </div>
      </header>

      <section className="hero">
        <div className="hero-badge">Intelligent Supply Network</div>
        <h1>
          Supply Chain Ontology &<br />
          <span className="gradient-text">Governed Analytics</span>
        </h1>
        <p className="hero-subtitle">
          A unified business ontology connecting every supply chain persona,
          from supplier to customer, through governed metrics and shared business definitions.
        </p>
        <button className="cta-btn" onClick={() => navigate('/dashboard')}>
          Explore Persona Intelligence <ArrowRight size={20} />
        </button>
      </section>
      <section className="principles-section">
        <div className="principles-grid">
          <div className="principle-card">
            <Link2 size={28} className="principle-icon" />
            <h3>Shared Ontology</h3>
            <p>One consistent model connecting entities from supplier to customer through governed relationships.</p>
          </div>
          <div className="principle-card">
            <Users size={28} className="principle-icon" />
            <h3>Multiple Personas</h3>
            <p>7 specialized views for procurement, manufacturing, warehouse, sales, logistics, quality, and finance.</p>
          </div>
          <div className="principle-card">
            <Database size={28} className="principle-icon" />
            <h3>Governed Metrics</h3>
            <p>Canonical metric definitions ensure consistent analytics across all personas and dashboards.</p>
          </div>
        </div>
      </section>

      <section className="metrics-section">
        <h2>Canonical Business Metrics</h2>
        <p className="section-subtitle">
          Shared definitions ensure every persona interprets metrics consistently.
        </p>
        <div className="metrics-grid">
          <div className="metric-def">
            <h4>On-Time Delivery</h4>
            <p>Percentage of deliveries completed on or before the committed date. Used by Procurement (supplier OTD), Sales (customer OTD), and Logistics (carrier OTD).</p>
          </div>
          <div className="metric-def">
            <h4>Fill Rate</h4>
            <p>Percentage of requested quantity successfully fulfilled. Sales measures order fill rate; Warehouse measures pick accuracy.</p>
          </div>
          <div className="metric-def">
            <h4>Days of Inventory</h4>
            <p>Average days current inventory can support expected demand. Finance for working capital.</p>
          </div>
          <div className="metric-def">
            <h4>Landed Cost</h4>
            <p>Total cost including purchase price, transportation, handling, and duties. Finance uses full landed cost; Procurement tracks PO price only.</p>
          </div>
        </div>
      </section>

      <section className="cta-section">
        <h2>One Supply Chain. Multiple Personas. One Governed Business Language.</h2>
        <p>Explore how each persona sees the same ontology from their unique perspective.</p>
        <button className="cta-btn" onClick={() => navigate('/dashboard')}>
          Explore Persona Intelligence <ArrowRight size={20} />
        </button>
      </section>

      <footer className="home-footer">
        <p>Supply Chain Ontology & Governed Analytics | Developed by Pro-Scientists</p>
      </footer>
    </div>
  );
}
