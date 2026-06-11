const BASE = import.meta.env.VITE_API_URL || '/api';

async function safeFetch(url, options) {
  try {
    return await fetch(url, options);
  } catch {
    throw new Error('BACKEND_OFFLINE');
  }
}

async function handleResponse(res) {
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    const msg = err.error || err.detail || '';
    if (res.status === 503 && /model file|not found/i.test(msg)) {
      throw new Error('MODEL_MISSING');
    }
    throw new Error(msg || `Request failed (HTTP ${res.status})`);
  }
  return res.json();
}

export async function fetchPrediction(formData) {
  const res = await safeFetch(`${BASE}/predict`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(formData),
  });
  return handleResponse(res);
}

export async function fetchModelInfo() {
  const res = await safeFetch(`${BASE}/model-info`);
  return handleResponse(res);
}

export async function fetchRegions() {
  const res = await safeFetch(`${BASE}/regions`);
  return handleResponse(res);
}

export async function fetchRegionWeather({ country, state, city }) {
  const url = new URL(`${BASE}/region-weather`, window.location.origin);
  url.searchParams.set('country', country);
  url.searchParams.set('state', state);
  url.searchParams.set('city', city);
  const res = await safeFetch(url.toString());
  return handleResponse(res);
}

export async function fetchWeatherByLocation({ latitude, longitude }) {
  const url = new URL(`${BASE}/current-weather`, window.location.origin);
  url.searchParams.set('latitude', latitude);
  url.searchParams.set('longitude', longitude);

  const res = await safeFetch(url.toString());
  const body = await handleResponse(res);
  return body.current_weather;
}

export async function fetchHealth() {
  const res = await safeFetch(`${BASE}/health`);
  return handleResponse(res);
}
