import {
  AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid
} from 'recharts';

const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null;
  return (
    <div style={{
      background: '#000', border: '3px solid #000',
      padding: '8px 12px', fontFamily: "'Space Mono',monospace",
      fontSize: 11, fontWeight: 700, color: '#FFE500', textTransform: 'uppercase',
    }}>
      <div style={{ color: '#fff', marginBottom: 4 }}>{label}</div>
      <div>₹{Number(payload[0].value).toLocaleString()}</div>
    </div>
  );
};

function RevenueTrendChart({ data }) {
  return (
    <div className="chart-card chart-full">
      <div className="chart-card-header">
        <span className="chart-card-header-dot blue" />
        <div>
          <div className="chart-card-title">Revenue Trend — Last 30 Days</div>
          <div className="chart-card-subtitle">Daily revenue from paid bills</div>
        </div>
      </div>
      <ResponsiveContainer width="100%" height={220}>
        <AreaChart data={data} margin={{ top: 4, right: 4, left: -10, bottom: 0 }}>
          <defs>
            <pattern id="brutalistHatch" patternUnits="userSpaceOnUse" width="8" height="8" patternTransform="rotate(45)">
              <line x1="0" y1="0" x2="0" y2="8" stroke="#000" strokeWidth="2" strokeOpacity="0.12" />
            </pattern>
          </defs>
          <CartesianGrid stroke="#000" strokeOpacity={0.08} strokeDasharray="4 4" vertical={false} />
          <XAxis
            dataKey="date"
            tick={{ fontFamily: "'Space Mono',monospace", fontSize: 9, fontWeight: 700, fill: '#000' }}
            axisLine={{ stroke: '#000', strokeWidth: 2 }}
            tickLine={{ stroke: '#000' }}
            interval={4}
          />
          <YAxis
            tick={{ fontFamily: "'Space Mono',monospace", fontSize: 9, fontWeight: 700, fill: '#000' }}
            axisLine={{ stroke: '#000', strokeWidth: 2 }}
            tickLine={{ stroke: '#000' }}
            tickFormatter={(v) => `₹${v}`}
          />
          <Tooltip content={<CustomTooltip />} />
          <Area
            type="monotone"
            dataKey="revenue"
            stroke="#000"
            strokeWidth={3}
            fill="url(#brutalistHatch)"
            dot={false}
            activeDot={{ r: 6, fill: '#FFE500', stroke: '#000', strokeWidth: 3 }}
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}

export default RevenueTrendChart;
