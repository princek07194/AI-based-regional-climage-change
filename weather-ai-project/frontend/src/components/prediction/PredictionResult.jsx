import { MapPin } from 'lucide-react';
import GlassCard from '../ui/GlassCard.jsx';
import { getWeatherIcon, RISK_COLORS } from '../../utils/weatherIcons.js';

function RiskBadge({ risk }) {
  if (!risk) return null;
  const color = RISK_COLORS[risk.level] || '#94a3b8';
  return (
    <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold"
      style={{ background: `${color}25`, color, border: `1px solid ${color}60` }}>
      {risk.icon} {risk.level} Risk
    </span>
  );
}

function ProbBar({ label, probability, rank }) {
  const colors = ['#38bdf8', '#818cf8', '#a78bfa', '#c084fc', '#e879f9'];
  return (
    <div className="space-y-1">
      <div className="flex justify-between text-xs">
        <span className="text-slate-300 truncate max-w-[65%]">{label}</span>
        <span className="font-bold" style={{ color: colors[rank] }}>{probability.toFixed(1)}%</span>
      </div>
      <div className="w-full bg-slate-700 rounded-full h-2">
        <div className="h-2 rounded-full transition-all duration-700"
          style={{ width: `${Math.min(probability, 100)}%`, background: colors[rank] }} />
      </div>
    </div>
  );
}

export default function PredictionResult({ result }) {
  const { prediction, region } = result;
  const top5 = prediction.top5 || prediction.top3 || [];
  const icon = getWeatherIcon(prediction.condition);

  return (
    <div className="space-y-6 animate-fadeIn">
      {region && (
        <GlassCard className="!py-4">
          <div className="flex flex-wrap items-center gap-4">
            <MapPin className="w-5 h-5 text-sky-400" />
            <div>
              <p className="text-xs text-slate-400 uppercase tracking-wide">Region Summary</p>
              <p className="text-white font-semibold">{region.location_label}</p>
              <p className="text-slate-400 text-sm">{region.climate_zone} · {region.latitude}°, {region.longitude}°</p>
            </div>
          </div>
        </GlassCard>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 glass rounded-2xl p-6"
          style={{ background: 'linear-gradient(135deg,rgba(14,165,233,0.12),rgba(99,102,241,0.08))' }}>
          <div className="flex items-start justify-between flex-wrap gap-4">
            <div>
              <p className="text-slate-400 text-sm mb-1">Predicted Condition</p>
              <div className="flex items-center gap-3 mb-2">
                <span className="text-4xl">{icon}</span>
                <h2 className="text-3xl font-black text-white">{prediction.condition}</h2>
              </div>
              <RiskBadge risk={prediction.risk} />
              {prediction.calibration?.applied && prediction.raw_model && (
                <p className="text-xs text-slate-400 mt-3 max-w-md">
                  Adjusted using your inputs (cloud {prediction.calibration.cloud ?? 0}%, rain {prediction.calibration.precip_mm ?? 0} mm).
                  Raw model: <span className="text-amber-300">{prediction.raw_model.condition}</span> ({prediction.raw_model.confidence?.toFixed(1)}%).
                </p>
              )}
            </div>
            <div className="text-right">
              <p className="text-slate-400 text-sm mb-1">Confidence</p>
              <div className="text-5xl font-black text-sky-400">{prediction.confidence.toFixed(1)}%</div>
            </div>
          </div>
          <div className="mt-6">
            <div className="flex justify-between text-xs text-slate-400 mb-1">
              <span>Model confidence</span>
              <span>{prediction.confidence.toFixed(1)}%</span>
            </div>
            <div className="w-full h-3 bg-slate-700 rounded-full overflow-hidden">
              <div className="h-3 rounded-full transition-all duration-1000"
                style={{ width: `${prediction.confidence}%`, background: 'linear-gradient(90deg,#0ea5e9,#6366f1)' }} />
            </div>
          </div>
        </div>

        <GlassCard>
          <h3 className="text-sm font-bold text-slate-300 mb-4">Top 5 Predictions</h3>
          <div className="space-y-4">
            {top5.map((t, i) => (
              <ProbBar key={t.class} label={t.condition} probability={t.probability} rank={i} />
            ))}
          </div>
        </GlassCard>
      </div>
    </div>
  );
}
