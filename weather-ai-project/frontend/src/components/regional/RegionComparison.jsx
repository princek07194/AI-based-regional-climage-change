import { useState } from 'react';
import { GitCompare, Loader2 } from 'lucide-react';
import GlassCard from '../ui/GlassCard.jsx';
import SectionTitle from '../ui/SectionTitle.jsx';
import { fetchPrediction } from '../../utils/api.js';

const PRESETS = [
  { label: 'Srinagar (Kashmir)', lat: 34.08, lon: 74.8, city: 'Srinagar', state: 'Jammu and Kashmir' },
  { label: 'Jaipur (Rajasthan)', lat: 26.91, lon: 75.79, city: 'Jaipur', state: 'Rajasthan' },
];

export default function RegionComparison({ weatherForm }) {
  const [rows, setRows] = useState(null);
  const [loading, setLoading] = useState(false);

  const compare = async () => {
    setLoading(true);
    try {
      const results = await Promise.all(
        PRESETS.map(async p => {
          const data = await fetchPrediction({
            ...weatherForm,
            country: 'India',
            state: p.state,
            city: p.city,
            latitude: p.lat,
            longitude: p.lon,
          });
          return { ...p, condition: data.prediction.condition, confidence: data.prediction.confidence };
        })
      );
      setRows(results);
    } catch {
      setRows(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <GlassCard>
      <SectionTitle icon={GitCompare} title="Region-wise Comparison" subtitle="Same weather inputs at two regions (bonus)" />
      <button type="button" onClick={compare} disabled={loading}
        className="mb-4 px-4 py-2 rounded-lg bg-indigo-600/80 text-white text-sm font-medium flex items-center gap-2">
        {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <GitCompare className="w-4 h-4" />}
        Compare Kashmir vs Rajasthan at {weatherForm.temperature_celsius}°C
      </button>
      {rows && (
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {rows.map(r => (
            <div key={r.label} className="rounded-xl p-4 bg-slate-800/60 border border-slate-600/40">
              <p className="text-slate-400 text-xs">{r.label}</p>
              <p className="text-white font-bold text-lg mt-1">{r.condition}</p>
              <p className="text-sky-400 text-sm">{r.confidence.toFixed(1)}% confidence</p>
              <p className="text-slate-500 text-xs mt-1">{r.lat}°, {r.lon}°</p>
            </div>
          ))}
        </div>
      )}
    </GlassCard>
  );
}
