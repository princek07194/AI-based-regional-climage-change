import { useState } from 'react';
import { LayoutGrid } from 'lucide-react';
import GlassCard from '../ui/GlassCard.jsx';
import SectionTitle from '../ui/SectionTitle.jsx';
import { getWeatherIcon } from '../../utils/weatherIcons.js';

export default function WeatherClassesGrid({ distribution, predictedClass }) {
  const [filter, setFilter] = useState('');
  if (!distribution?.length) return null;

  const items = distribution
    .filter(c => !filter || c.condition.toLowerCase().includes(filter.toLowerCase()))
    .sort((a, b) => b.probability - a.probability);

  return (
    <GlassCard>
      <SectionTitle icon={LayoutGrid} title="Weather Class Visualization" subtitle="All 48 classes — predicted class highlighted" />
      <input
        type="search"
        placeholder="Filter conditions…"
        value={filter}
        onChange={e => setFilter(e.target.value)}
        className="w-full mb-4 rounded-xl bg-slate-800/80 border border-slate-600/50 text-white text-sm px-4 py-2"
      />
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-2 max-h-96 overflow-y-auto pr-1">
        {items.map(c => {
          const active = c.class === predictedClass;
          return (
            <div
              key={c.class}
              className={`rounded-lg px-2 py-2 text-center text-xs transition-all ${
                active
                  ? 'bg-sky-500/30 border-2 border-sky-400 scale-105 shadow-lg shadow-sky-500/20'
                  : 'bg-slate-800/50 border border-slate-700/50 opacity-80 hover:opacity-100'
              }`}
            >
              <div className="text-lg">{getWeatherIcon(c.condition)}</div>
              <p className={`font-medium truncate ${active ? 'text-white' : 'text-slate-400'}`}>{c.condition}</p>
              <p className={`font-mono mt-0.5 ${active ? 'text-sky-300' : 'text-slate-500'}`}>{c.probability.toFixed(1)}%</p>
            </div>
          );
        })}
      </div>
    </GlassCard>
  );
}
