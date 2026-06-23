import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';

// Brutalist palette — stark primaries
const BAR_COLORS = ['#000000', '#FFE500', '#FF2D00', '#0041FF', '#00C14D'];

const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null;
  return (
    <div style={{
      background: '#000',
      border: '3px solid #000',
      padding: '8px 12px',
      fontFamily: "'Space Mono', monospace",
      fontSize: '11px',
      fontWeight: 700,
      color: '#FFE500',
      textTransform: 'uppercase',
      letterSpacing: '0.5px',
    }}>
      <div style={{ color: '#fff', marginBottom: 4 }}>{label}</div>
      <div>{payload[0].value} SOLD</div>
    </div>
  );
};

function BestSellersChart({ data }) {
  return (
    <div className="chart-card">
      <div className="chart-card-header">
        <span className="chart-card-header-dot yellow" />
        <div>
          <div className="chart-card-title">Best Sellers</div>
          <div className="chart-card-subtitle">Top items by qty sold</div>
        </div>
      </div>
      <ResponsiveContainer width="100%" height={260}>
        <BarChart data={data} margin={{ top: 4, right: 4, left: -16, bottom: 0 }}
          barCategoryGap="28%">
          <XAxis
            dataKey="name"
            tick={{ fontFamily: "'Space Mono',monospace", fontSize: 9, fontWeight: 700, fill: '#000' }}
            axisLine={{ stroke: '#000', strokeWidth: 2 }}
            tickLine={{ stroke: '#000' }}
          />
          <YAxis
            tick={{ fontFamily: "'Space Mono',monospace", fontSize: 9, fontWeight: 700, fill: '#000' }}
            axisLine={{ stroke: '#000', strokeWidth: 2 }}
            tickLine={{ stroke: '#000' }}
          />
          <Tooltip content={<CustomTooltip />} cursor={{ fill: 'rgba(0,0,0,0.05)' }} />
          <Bar dataKey="quantity_sold" radius={0} stroke="#000" strokeWidth={2}>
            {data && data.map((_, i) => (
              <Cell key={i} fill={BAR_COLORS[i % BAR_COLORS.length]} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

export default BestSellersChart;
