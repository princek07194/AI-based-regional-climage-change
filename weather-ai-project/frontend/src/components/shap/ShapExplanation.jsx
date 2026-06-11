import { useState } from 'react';
import { Brain, CheckCircle, ChevronDown, ChevronUp, MapPin } from 'lucide-react';
import GlassCard from '../ui/GlassCard.jsx';
import SectionTitle from '../ui/SectionTitle.jsx';
import { BAR_POS, BAR_NEG } from '../../utils/weatherIcons.js';

function ShapBar({ record }) {
  const val = record.shap_value;
  const isPos = val >= 0;
  const pct = Math.min(Math.abs(val) * 400, 100);
  return (
    <div className={`flex items-center gap-3 py-1.5 px-1 ${record.is_regional ? 'ring-1 ring-amber-400/40 rounded' : ''}`}>
      <div className="w-36 text-xs text-slate-300 truncate text-right" title={record.feature}>
        {record.feature.replace(/_/g, ' ')}
        {record.is_regional && <span className="text-amber-400 ml-1">📍</span>}
      </div>
      <div className="flex-1 flex items-center">
        {isPos ? (
          <div className="flex-1 flex justify-start">
            <div className="h-4 rounded-r-full" style={{ width: `${pct}%`, background: BAR_POS, minWidth: 4 }} />
          </div>
        ) : (
          <div className="flex-1 flex justify-end">
            <div className="h-4 rounded-l-full" style={{ width: `${pct}%`, background: BAR_NEG, minWidth: 4 }} />
          </div>
        )}
      </div>
      <div className="w-16 text-xs text-right font-mono" style={{ color: isPos ? BAR_POS : BAR_NEG }}>
        {isPos ? '+' : ''}{val.toFixed(4)}
      </div>
    </div>
  );
}

export default function ShapExplanation({ explanation }) {
  const [showAll, setShowAll] = useState(false);
  if (!explanation || explanation.error) return null;

  const regional = explanation.regional_analysis;
  const rows = showAll ? explanation.shap_values : explanation.shap_values?.slice(0, 8);

  return (
    <GlassCard>
      <SectionTitle icon={Brain} title="SHAP Explainability" subtitle="Feature contributions including regional latitude/longitude" />

      <div className="mb-6 p-4 rounded-xl bg-sky-500/10 border border-sky-500/20">
        <div className="flex items-start gap-3">
          <CheckCircle className="w-5 h-5 text-sky-400 shrink-0 mt-0.5" />
          <p className="text-sky-100 text-sm leading-relaxed">{explanation.natural_language}</p>
        </div>
      </div>

      {regional?.features?.length > 0 && (
        <div className="mb-6 p-4 rounded-xl bg-amber-500/10 border border-amber-500/25">
          <div className="flex items-center gap-2 mb-2">
            <MapPin className="w-4 h-4 text-amber-400" />
            <p className="text-amber-200 text-sm font-bold">Regional Contribution Analysis</p>
          </div>
          <p className="text-slate-300 text-xs mb-3">{regional.summary}</p>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
            {regional.features.map(r => (
              <div key={r.feature} className="flex justify-between text-xs bg-slate-800/50 rounded-lg px-3 py-2">
                <span className="text-slate-300">{r.feature} = {r.value}</span>
                <span className="text-amber-300 font-mono">
                  {r.shap_value > 0 ? '+' : ''}{r.shap_value.toFixed(4)} ({r.contribution_pct}%)
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="flex gap-6 mb-4 text-xs text-slate-400 flex-wrap">
        <span className="flex items-center gap-2"><span className="w-3 h-3 rounded-sm" style={{ background: BAR_POS }} /> Increased</span>
        <span className="flex items-center gap-2"><span className="w-3 h-3 rounded-sm" style={{ background: BAR_NEG }} /> Decreased</span>
        <span className="text-amber-400">📍 regional feature</span>
      </div>

      <div className="space-y-1">{rows?.map(r => <ShapBar key={r.feature} record={r} />)}</div>

      {explanation.shap_values?.length > 8 && (
        <button type="button" onClick={() => setShowAll(s => !s)} className="mt-4 flex items-center gap-1 text-sky-400 text-sm">
          {showAll ? <><ChevronUp className="w-4 h-4" /> Show less</> : <><ChevronDown className="w-4 h-4" /> Show all</>}
        </button>
      )}

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mt-8">
        <div className="rounded-xl p-4" style={{ background: 'rgba(56,189,248,0.08)', border: '1px solid rgba(56,189,248,0.15)' }}>
          <p className="text-xs font-bold text-sky-400 mb-3 uppercase">↑ Positive</p>
          {explanation.top_positive?.map(r => (
            <div key={r.feature} className="flex justify-between text-xs py-1 border-b border-sky-500/10">
              <span className="text-slate-300">{r.feature.replace(/_/g, ' ')}</span>
              <span className="text-sky-400 font-mono">+{r.shap_value.toFixed(4)}</span>
            </div>
          ))}
        </div>
        <div className="rounded-xl p-4" style={{ background: 'rgba(248,113,113,0.08)', border: '1px solid rgba(248,113,113,0.15)' }}>
          <p className="text-xs font-bold text-red-400 mb-3 uppercase">↓ Negative</p>
          {explanation.top_negative?.map(r => (
            <div key={r.feature} className="flex justify-between text-xs py-1 border-b border-red-500/10">
              <span className="text-slate-300">{r.feature.replace(/_/g, ' ')}</span>
              <span className="text-red-400 font-mono">{r.shap_value.toFixed(4)}</span>
            </div>
          ))}
        </div>
      </div>
    </GlassCard>
  );
}
