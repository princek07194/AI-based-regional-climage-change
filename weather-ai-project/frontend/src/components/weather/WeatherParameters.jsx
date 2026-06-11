import { Cloud, Thermometer, Droplets, Wind, Gauge, Eye, CloudRain, Activity, Loader2, AlertTriangle } from 'lucide-react';
import GlassCard from '../ui/GlassCard.jsx';
import SectionTitle from '../ui/SectionTitle.jsx';
import InputSlider from '../ui/InputSlider.jsx';

export default function WeatherParameters({ form, onChange, onSubmit, loading, error }) {
  return (
    <GlassCard>
      <SectionTitle icon={Cloud} title="Weather Parameters" subtitle="Adjust sliders for current atmospheric conditions" />
      <form onSubmit={onSubmit}>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
          <InputSlider label="Temperature" icon={Thermometer} name="temperature_celsius" value={form.temperature_celsius} onChange={onChange} min={-30} max={55} step={0.5} unit="°C" />
          <InputSlider label="Humidity" icon={Droplets} name="humidity" value={form.humidity} onChange={onChange} min={0} max={100} unit="%" />
          <InputSlider label="Wind Speed" icon={Wind} name="wind_mph" value={form.wind_mph} onChange={onChange} min={0} max={120} unit=" mph" />
          <InputSlider label="Pressure" icon={Gauge} name="pressure_mb" value={form.pressure_mb} onChange={onChange} min={900} max={1080} unit=" mb" />
          <InputSlider label="Visibility" icon={Eye} name="visibility_km" value={form.visibility_km} onChange={onChange} min={0} max={50} unit=" km" />
          <InputSlider label="Precipitation" icon={CloudRain} name="precip_mm" value={form.precip_mm} onChange={onChange} min={0} max={100} step={0.5} unit=" mm" />
          <InputSlider label="Cloud Cover" icon={Cloud} name="cloud" value={form.cloud} onChange={onChange} min={0} max={100} unit="%" />
        </div>

        {error && (
          <div className="mt-6 flex items-center gap-3 p-4 rounded-xl bg-red-500/10 border border-red-500/30 text-red-400">
            <AlertTriangle className="w-5 h-5 shrink-0" />
            <span className="text-sm">{error}</span>
          </div>
        )}

        <button
          type="submit"
          disabled={loading}
          className="mt-8 w-full py-4 rounded-xl font-bold text-white text-lg transition-all duration-200 active:scale-95 disabled:opacity-60 flex items-center justify-center gap-3"
          style={{ background: loading ? '#334155' : 'linear-gradient(135deg,#0ea5e9,#6366f1)' }}
        >
          {loading ? <><Loader2 className="w-5 h-5 animate-spin" />Analysing…</> : <><Activity className="w-5 h-5" />Predict Weather Condition</>}
        </button>
      </form>
    </GlassCard>
  );
}
