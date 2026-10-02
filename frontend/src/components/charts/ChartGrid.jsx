import {
  BarChart, Bar, LineChart, Line, PieChart, Pie, Cell,
  XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid
} from 'recharts';
import './ChartGrid.css';

const COLORS = ['#6366f1', '#10b981', '#f59e0b', '#ef4444', '#3b82f6', '#8b5cf6', '#06b6d4', '#f97316'];

function formatLabel(label) {
  if (!label) return '';
  const s = String(label);
  if (s.length > 20) return s.slice(0, 18) + '...';
  return s;
}

function ChartCard({ chart }) {
  const data = (chart.data || []).map(d => ({
    ...d,
    LABEL: d.LABEL || d.label || '',
    VALUE: Number(d.VALUE ?? d.value ?? 0),
    VALUE2: d.VALUE2 != null ? Number(d.VALUE2) : (d.value2 != null ? Number(d.value2) : undefined),
  }));

  if (data.length === 0) {
    return (
      <div className="chart-card">
        <h4 className="chart-title">{chart.title}</h4>
        <div className="chart-empty">No data available</div>
      </div>
    );
  }

  return (
    <div className="chart-card">
      <h4 className="chart-title">{chart.title}</h4>
      <div className="chart-body">
        {chart.type === 'bar' && (
          <ResponsiveContainer width="100%" height={240}>
            <BarChart data={data} margin={{ top: 8, right: 8, bottom: 40, left: 8 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
              <XAxis dataKey="LABEL" tick={{ fontSize: 10, fill: 'var(--text-muted)' }} angle={-25} textAnchor="end" />
              <YAxis tick={{ fontSize: 10, fill: 'var(--text-muted)' }} />
              <Tooltip contentStyle={{ background: 'var(--bg-tertiary)', border: '1px solid var(--border)', borderRadius: 8, fontSize: 12 }} />
              <Bar dataKey="VALUE" fill="#6366f1" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        )}
        {chart.type === 'line' && (
          <ResponsiveContainer width="100%" height={240}>
            <LineChart data={data} margin={{ top: 8, right: 8, bottom: 40, left: 8 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
              <XAxis dataKey="LABEL" tick={{ fontSize: 10, fill: 'var(--text-muted)' }} angle={-25} textAnchor="end" />
              <YAxis tick={{ fontSize: 10, fill: 'var(--text-muted)' }} />
              <Tooltip contentStyle={{ background: 'var(--bg-tertiary)', border: '1px solid var(--border)', borderRadius: 8, fontSize: 12 }} />
              <Line type="monotone" dataKey="VALUE" stroke="#6366f1" strokeWidth={2} dot={{ r: 3 }} />
              {data[0]?.VALUE2 !== undefined && (
                <Line type="monotone" dataKey="VALUE2" stroke="#10b981" strokeWidth={2} dot={{ r: 3 }} />
              )}
            </LineChart>
          </ResponsiveContainer>
        )}
        {chart.type === 'pie' && (
          <ResponsiveContainer width="100%" height={240}>
            <PieChart>
              <Pie
                data={data}
                dataKey="VALUE"
                nameKey="LABEL"
                cx="50%"
                cy="50%"
                innerRadius={50}
                outerRadius={90}
                paddingAngle={2}
              >
                {data.map((_, i) => (
                  <Cell key={i} fill={COLORS[i % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip contentStyle={{ background: 'var(--bg-tertiary)', border: '1px solid var(--border)', borderRadius: 8, fontSize: 12 }} />
            </PieChart>
          </ResponsiveContainer>
        )}
      </div>
    </div>
  );
}

export default function ChartGrid({ charts }) {
  if (!charts || charts.length === 0) return null;

  return (
    <div className="charts-section">
      <h3 className="section-title">Analytics & Trends</h3>
      <div className="charts-grid">
        {charts.map((chart) => (
          <ChartCard key={chart.id} chart={chart} />
        ))}
      </div>
    </div>
  );
}
