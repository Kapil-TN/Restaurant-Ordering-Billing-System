import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const COLORS = ['#000000', '#FFE500'];
const OUTER_COLORS_STROKE = ['#000', '#000'];

const RADIAN = Math.PI / 180;
const CustomLabel = ({ cx, cy, midAngle, innerRadius, outerRadius, percent, name }) => {
  const radius = innerRadius + (outerRadius - innerRadius) * 0.5;
  const x = cx + radius * Math.cos(-midAngle * RADIAN);
  const y = cy + radius * Math.sin(-midAngle * RADIAN);
  return (
    <text
      x={x} y={y}
      textAnchor="middle"
      dominantBaseline="central"
      style={{ fontFamily: "'Space Mono',monospace", fontSize: 11, fontWeight: 700 }}
      fill={percent > 0.5 ? '#FFE500' : '#000'}
    >
      {`${(percent * 100).toFixed(0)}%`}
    </text>
  );
};

const CustomTooltip = ({ active, payload }) => {
  if (!active || !payload?.length) return null;
  return (
    <div style={{
      background: '#000', border: '3px solid #000',
      padding: '8px 12px', fontFamily: "'Space Mono',monospace",
      fontSize: 11, fontWeight: 700, color: '#FFE500', textTransform: 'uppercase',
    }}>
      <div style={{ color: '#fff', marginBottom: 4 }}>{payload[0].name}</div>
      <div>{payload[0].value} ORDERS</div>
    </div>
  );
};

const CustomLegend = ({ payload }) => (
  <div style={{ display: 'flex', gap: '1.2rem', justifyContent: 'center', marginTop: 10 }}>
    {payload.map((entry, i) => (
      <div key={i} style={{ display: 'flex', alignItems: 'center', gap: 6,
        fontFamily: "'Space Mono',monospace", fontSize: 10, fontWeight: 700,
        textTransform: 'uppercase', letterSpacing: 1 }}>
        <span style={{
          width: 14, height: 14, background: entry.color,
          border: '2px solid #000', display: 'inline-block', flexShrink: 0
        }} />
        {entry.value}
      </div>
    ))}
  </div>
);

function OrderTypePieChart({ data }) {
  return (
    <div className="chart-card">
      <div className="chart-card-header">
        <span className="chart-card-header-dot red" />
        <div>
          <div className="chart-card-title">Order Types</div>
          <div className="chart-card-subtitle">Dine-in vs takeaway split</div>
        </div>
      </div>
      <ResponsiveContainer width="100%" height={260}>
        <PieChart>
          <Pie
            data={data}
            dataKey="count"
            nameKey="order_type"
            cx="50%" cy="48%"
            outerRadius={95}
            innerRadius={0}
            labelLine={false}
            label={CustomLabel}
            strokeWidth={3}
            stroke="#000"
          >
            {data && data.map((entry, i) => (
              <Cell key={entry.order_type} fill={COLORS[i % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip content={<CustomTooltip />} />
          <Legend content={<CustomLegend />} />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}

export default OrderTypePieChart;
