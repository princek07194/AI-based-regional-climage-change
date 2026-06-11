import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { Info, Activity } from 'lucide-react';
import GlassCard from '../ui/GlassCard.jsx';
import SectionTitle from '../ui/SectionTitle.jsx';

export default function ModelInfoSection({ modelInfo }) {
  if (!modelInfo) return null;
  const chartData = modelInfo.top_features?.slice(0, 12) || [];

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <GlassCard>
        <SectionTitle icon={Info} title="Model Information" />
        <div className="space-y-3">
          {[
            ['Model Name', modelInfo.model_name],
            ['Algorithm', modelInfo.algorithm],
            ['Objective', modelInfo.objective],
            ['Estimators', modelInfo.n_estimators],
            ['Max Depth', modelInfo.max_depth],
            ['Learning Rate', modelInfo.learning_rate],
            ['Input Features', modelInfo.n_features],
            ['Output Classes', modelInfo.n_classes],
            ['Region Aware', modelInfo.dataset_info?.region_aware ? '✅ Yes' : '—'],
            ['XAI', modelInfo.xai_enabled ? '✅ SHAP Enabled' : '❌'],
          ].map(([k, v]) => (
            <div key={k} className="flex justify-between py-2 border-b border-slate-700/50 text-sm">
              <span className="text-slate-400">{k}</span>
              <span className="text-white font-medium text-right max-w-[55%]">{String(v)}</span>
            </div>
          ))}
        </div>
      </GlassCard>

      <GlassCard>
        <SectionTitle icon={Activity} title="Feature Importance" subtitle="Top features by XGBoost F-score" />
        <ResponsiveContainer width="100%" height={340}>
          <BarChart data={chartData} layout="vertical" margin={{ top: 0, right: 16, bottom: 0, left: 110 }}>
            <XAxis type="number" tick={{ fill: '#94a3b8', fontSize: 11 }} axisLine={false} tickLine={false} />
            <YAxis type="category" dataKey="feature" tick={{ fill: '#cbd5e1', fontSize: 10 }} axisLine={false} tickLine={false}
              tickFormatter={f => f.replace(/_/g, ' ')} />
            <Tooltip contentStyle={{ background: '#1e293b', border: '1px solid #334155', borderRadius: 8 }}
              formatter={v => [v.toLocaleString(), 'F-score']} />
            <Bar dataKey="importance" radius={[0, 4, 4, 0]}>
              {chartData.map((_, i) => (
                <Cell key={i} fill={`hsl(${200 + i * 8}, 80%, ${65 - i * 2}%)`} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </GlassCard>
    </div>
  );
}
