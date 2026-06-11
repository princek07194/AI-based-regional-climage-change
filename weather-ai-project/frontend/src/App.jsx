import { useState, useEffect } from 'react';
import { fetchPrediction, fetchModelInfo, fetchRegionWeather, fetchWeatherByLocation } from './utils/api.js';
import Hero from './components/layout/Hero.jsx';
import RegionalInfo from './components/regional/RegionalInfo.jsx';
import { DEFAULT_REGION } from './data/defaultRegion.js';
import WeatherParameters from './components/weather/WeatherParameters.jsx';
import PredictionResult from './components/prediction/PredictionResult.jsx';
import WeatherClassesGrid from './components/prediction/WeatherClassesGrid.jsx';
import ShapExplanation from './components/shap/ShapExplanation.jsx';
import ModelInfoSection from './components/model/ModelInfoSection.jsx';
import RegionComparison from './components/regional/RegionComparison.jsx';
import LoadingOverlay from './components/ui/LoadingOverlay.jsx';

const INITIAL_WEATHER = {
  temperature_celsius: 25,
  humidity: 60,
  wind_mph: 10,
  pressure_mb: 1013,
  visibility_km: 10,
  precip_mm: 0,
  cloud: 50,
};

export default function App() {
  const [region, setRegion] = useState(DEFAULT_REGION);
  const [weather, setWeather] = useState(INITIAL_WEATHER);
  const [result, setResult] = useState(null);
  const [modelInfo, setModelInfo] = useState(null);
  const [backendOffline, setBackendOffline] = useState(false);
  const [modelMissing, setModelMissing] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [weatherSource, setWeatherSource] = useState('manual');

  useEffect(() => {
    fetchModelInfo()
      .then(data => {
        setModelInfo(data);
        setModelMissing(false);
        setBackendOffline(false);
      })
      .catch(err => {
        setModelInfo(null);
        if (err.message === 'MODEL_MISSING') {
          setModelMissing(true);
          setBackendOffline(false);
        } else if (err.message === 'BACKEND_OFFLINE') {
          setBackendOffline(true);
          setModelMissing(false);
        } else {
          setBackendOffline(true);
          setModelMissing(false);
        }
      });
  }, []);

  const runPrediction = async (regionPayload, weatherPayload = weather) => {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const payload = {
        ...weatherPayload,
        country: regionPayload.country,
        state: regionPayload.state,
        city: regionPayload.city,
        latitude: regionPayload.latitude,
        longitude: regionPayload.longitude,
        climate_zone: regionPayload.climate_zone,
      };
      const data = await fetchPrediction(payload);
      setResult(data);
      setTimeout(() => document.getElementById('results')?.scrollIntoView({ behavior: 'smooth' }), 150);
    } catch (err) {
      if (err.message === 'BACKEND_OFFLINE') {
        setError('Backend is not running. Open a new terminal and run: npm run dev:backend');
      } else if (err.message === 'MODEL_MISSING') {
        setError('Model file not found in backend/model_store/weather_prediction_model.pkl');
      } else {
        setError(err.message);
      }
    } finally {
      setLoading(false);
    }
  };

  const loadWeatherForRegion = async regionPayload => {
    if (regionPayload.latitude == null || regionPayload.longitude == null) {
      setWeatherSource('manual');
      return null;
    }

    setError(null);
    setWeatherSource('fetching');
    try {
      const apiWeather = await fetchWeatherByLocation({
        latitude: regionPayload.latitude,
        longitude: regionPayload.longitude,
      });
      const mergedWeather = {
        ...weather,
        ...apiWeather,
      };
      setWeather(mergedWeather);
      setWeatherSource('live');
      return mergedWeather;
    } catch (err) {
      setError(`Could not fetch live weather for this region: ${err.message}`);
      setWeatherSource('manual');
      return null;
    }
  };

  const handleRegionChange = async regionPayload => {
    setRegion(regionPayload);

    const dbResult = await fetchRegionWeather(regionPayload)
      .then(data => data.region_weather)
      .catch(() => null);

    if (dbResult) {
      const regionWeather = {
        temperature_celsius: Number(dbResult.temperature_celsius),
        humidity: Number(dbResult.humidity),
        wind_mph: Number(dbResult.wind_mph),
        pressure_mb: Number(dbResult.pressure_mb),
        visibility_km: Number(dbResult.visibility_km),
        precip_mm: Number(dbResult.precip_mm),
        cloud: Number(dbResult.cloud),
      };
      setWeather(regionWeather);
      setWeatherSource('db');
      if (backendOffline || modelMissing) return;
      await runPrediction(regionPayload, regionWeather);
      return;
    }

    const mergedWeather = await loadWeatherForRegion(regionPayload);
    if (backendOffline || modelMissing) return;
    await runPrediction(regionPayload, mergedWeather || weather);
  };

  const handleWeatherChange = e => {
    const { name, value } = e.target;
    setWeather(prev => ({ ...prev, [name]: parseFloat(value) }));
  };

  const handleSubmit = async e => {
    e.preventDefault();
    await runPrediction(region);
  };

  return (
    <div className="min-h-screen dark" style={{ background: 'linear-gradient(135deg,#0a1628 0%,#0d1f3c 50%,#0a1628 100%)' }}>
      {loading && <LoadingOverlay />}
      <Hero />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 pb-20 space-y-8">
        {backendOffline && (
          <div className="rounded-xl p-4 bg-red-500/15 border border-red-500/40 text-red-100 text-sm">
            <strong>Backend not running.</strong> Open a second terminal and run:{' '}
            <code className="text-red-200">npm run dev:backend</code> (keep frontend running with <code className="text-red-200">npm run dev</code>).
          </div>
        )}
        {modelMissing && !backendOffline && (
          <div className="rounded-xl p-4 bg-amber-500/15 border border-amber-500/40 text-amber-100 text-sm">
            <strong>ML model missing.</strong> Place <code className="text-amber-200">weather_prediction_model.pkl</code> in{' '}
            <code className="text-amber-200">weather-ai-project/backend/model_store/</code> then restart the backend.
          </div>
        )}
        <RegionalInfo region={region} onChange={handleRegionChange} />
        {weatherSource === 'db' && (
          <div className="rounded-xl p-4 bg-emerald-500/10 border border-emerald-500/20 text-emerald-200 text-sm">
            Region values were loaded from the database and applied to the input sliders.
          </div>
        )}
        {weatherSource === 'live' && (
          <div className="rounded-xl p-4 bg-sky-500/10 border border-sky-500/20 text-sky-200 text-sm">
            Live current weather values were fetched for this region and applied to the sliders.
          </div>
        )}
        {weatherSource === 'fetching' && (
          <div className="rounded-xl p-4 bg-slate-800/80 border border-slate-600/40 text-slate-300 text-sm">
            Fetching current region weather to auto-fill input values…
          </div>
        )}
        <WeatherParameters form={weather} onChange={handleWeatherChange} onSubmit={handleSubmit} loading={loading} error={error} />

        {result && (
          <div id="results" className="space-y-8">
            <PredictionResult result={result} />
            <WeatherClassesGrid
              distribution={result.prediction.probability_distribution}
              predictedClass={result.prediction.class}
            />
            <ShapExplanation explanation={result.explanation} />
            <RegionComparison weatherForm={weather} />
          </div>
        )}

        <ModelInfoSection modelInfo={modelInfo} />
      </main>

      <footer className="text-center py-8 text-slate-600 text-xs">
        RegionalClimate XAI · Region-Aware · XGBoost + SHAP · React &amp; Flask
      </footer>
    </div>
  );
}
