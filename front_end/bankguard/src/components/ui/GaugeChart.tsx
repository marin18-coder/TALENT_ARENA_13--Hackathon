import React, { useMemo } from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer } from 'recharts';

interface GaugeChartProps {
  score: number;
}

export const GaugeChart: React.FC<GaugeChartProps> = ({ score }) => {
  const data = useMemo(() => [
    { name: 'Score', value: score },
    { name: 'Remaining', value: 100 - score },
  ], [score]);
  
  const color = useMemo(() => {
    if (score < 30) return '#10b981';
    if (score < 60) return '#f59e0b';
    return '#ef4444';
  }, [score]);

  return (
    <div className="h-48 w-48 relative">
      <ResponsiveContainer width="100%" height="100%">
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            innerRadius={100}
            outerRadius={80}
            startAngle={180}
            endAngle={0}
            paddingAngle={0}
            dataKey="value"
            stroke="none"
          >
            <Cell fill={color} />
            <Cell fill="#f1f5f9" />
          </Pie>
        </PieChart>
      </ResponsiveContainer>
      <div className="absolute inset-0 flex flex-col items-center justify-center pt-8">
        <span className="text-4xl font-bold tabular-nums">{score}</span>
        <span className="text-[10px] text-slate-400 uppercase tracking-[0.2em] font-mono font-bold">Risk Index</span>
      </div>
    </div>
  );
};
