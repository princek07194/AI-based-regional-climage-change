import { useEffect, useState } from 'react';
import { MapPin, Navigation, Globe, Loader2 } from 'lucide-react';
import GlassCard from '../ui/GlassCard.jsx';
import SectionTitle from '../ui/SectionTitle.jsx';
import { fetchRegions } from '../../utils/api.js';
import { detectGpsLocation, inferClimateZone } from '../../utils/regions.js';
import { FALLBACK_COUNTRIES } from '../../data/regionsFallback.js';

export default function RegionalInfo({ region, onChange }) {
  const [catalog, setCatalog] = useState(null);
  const [gpsLoading, setGpsLoading] = useState(false);
  const [gpsError, setGpsError] = useState(null);

  useEffect(() => {
    fetchRegions()
      .then(data => setCatalog(data.countries))
      .catch(() => setCatalog(null));
  }, []);

  const countries = catalog?.length ? catalog : FALLBACK_COUNTRIES;
  const countryObj = countries.find(c => c.name === region.country) || countries[0];
  const states = countryObj?.states || [];
  const stateObj = states.find(s => s.name === region.state) || states[0];
  const cities = stateObj?.cities || [];

  const setRegion = patch => onChange({ ...region, ...patch });

  const handleCountry = e => {
    const name = e.target.value;
    const c = countries.find(x => x.name === name);
    const st = c?.states?.[0];
    const city = st?.cities?.[0];
    setRegion({
      country: name,
      state: st?.name || '',
      city: city?.name || '',
      latitude: city?.latitude ?? 20,
      longitude: city?.longitude ?? 78,
      climate_zone: city?.climate_zone || inferClimateZone(city?.latitude ?? 20),
    });
  };

  const handleState = e => {
    const name = e.target.value;
    const st = states.find(x => x.name === name);
    const city = st?.cities?.[0];
    setRegion({
      state: name,
      city: city?.name || '',
      latitude: city?.latitude ?? region.latitude,
      longitude: city?.longitude ?? region.longitude,
      climate_zone: city?.climate_zone || inferClimateZone(city?.latitude ?? region.latitude),
    });
  };

  const handleCity = e => {
    const name = e.target.value;
    const city = cities.find(x => x.name === name);
    if (!city) return;
    setRegion({
      city: name,
      latitude: city.latitude,
      longitude: city.longitude,
      climate_zone: city.climate_zone,
    });
  };

  const handleGps = async () => {
    setGpsLoading(true);
    setGpsError(null);
    try {
      const { latitude, longitude } = await detectGpsLocation();
      setRegion({
        city: '',
        latitude,
        longitude,
        climate_zone: inferClimateZone(latitude),
      });
    } catch (err) {
      setGpsError(err.message);
    } finally {
      setGpsLoading(false);
    }
  };

  const selectClass =
    'w-full rounded-xl bg-slate-800/80 border border-slate-600/50 text-white text-sm px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-sky-500/50';

  return (
    <GlassCard>
      <SectionTitle
        icon={Globe}
        title="Regional Information"
        subtitle="Location drives latitude/longitude features — same weather differs by region"
      />

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="space-y-4">
          <label className="block text-xs text-slate-400 uppercase tracking-wide">Country</label>
          <select className={selectClass} value={region.country || ''} onChange={handleCountry}>
            {countries.map(c => (
              <option key={c.name} value={c.name}>{c.name}</option>
            ))}
          </select>

          <label className="block text-xs text-slate-400 uppercase tracking-wide">State / Province</label>
          <select className={selectClass} value={region.state || ''} onChange={handleState}>
            {states.map(s => (
              <option key={s.name} value={s.name}>{s.name}</option>
            ))}
          </select>

          <label className="block text-xs text-slate-400 uppercase tracking-wide">City</label>
          <select className={selectClass} value={region.city || ''} onChange={handleCity}>
            {cities.map(c => (
              <option key={c.name} value={c.name}>{c.name}</option>
            ))}
            <option value="">— Custom / GPS —</option>
          </select>

          <button
            type="button"
            onClick={handleGps}
            disabled={gpsLoading}
            className="w-full flex items-center justify-center gap-2 py-2.5 rounded-xl border border-sky-500/40 text-sky-300 hover:bg-sky-500/10 transition-colors text-sm font-medium"
          >
            {gpsLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Navigation className="w-4 h-4" />}
            Auto-detect GPS location
          </button>
          {gpsError && <p className="text-red-400 text-xs">{gpsError}</p>}
        </div>

        <div className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs text-slate-400 mb-1">Latitude</label>
              <input
                type="number"
                step="0.0001"
                className={selectClass}
                value={region.latitude}
                onChange={e => setRegion({
                  latitude: parseFloat(e.target.value) || 0,
                  climate_zone: inferClimateZone(parseFloat(e.target.value) || 0),
                })}
              />
            </div>
            <div>
              <label className="block text-xs text-slate-400 mb-1">Longitude</label>
              <input
                type="number"
                step="0.0001"
                className={selectClass}
                value={region.longitude}
                onChange={e => setRegion({ longitude: parseFloat(e.target.value) || 0 })}
              />
            </div>
          </div>

          <div>
            <label className="block text-xs text-slate-400 mb-1">Climate Zone (optional)</label>
            <input
              type="text"
              className={selectClass}
              value={region.climate_zone || ''}
              onChange={e => setRegion({ climate_zone: e.target.value })}
              placeholder="e.g. Subtropical"
            />
          </div>

          <div className="rounded-xl p-4 bg-sky-500/10 border border-sky-500/20 flex items-start gap-3">
            <MapPin className="w-5 h-5 text-sky-400 shrink-0 mt-0.5" />
            <div className="text-sm">
              <p className="text-white font-semibold">
                {[region.city, region.state, region.country].filter(Boolean).join(', ') || 'Custom location'}
              </p>
              <p className="text-slate-400 mt-1">
                {region.latitude?.toFixed(4)}°, {region.longitude?.toFixed(4)}° · {region.climate_zone}
              </p>
              <p className="text-sky-300/80 text-xs mt-2">
                Example: 25°C in Kashmir vs Rajasthan uses different lat/lon in the model.
              </p>
            </div>
          </div>
        </div>
      </div>
    </GlassCard>
  );
}
