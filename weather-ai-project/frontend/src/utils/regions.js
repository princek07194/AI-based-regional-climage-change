/** Infer climate zone from latitude when not provided by API/city data. */
export function inferClimateZone(lat) {
  if (lat >= 32) return 'Alpine / Himalayan';
  if (lat >= 23.5) return 'Subtropical';
  if (lat >= 15) return 'Tropical Wet & Dry';
  return 'Tropical';
}

/** Browser geolocation → { latitude, longitude }. */
export function detectGpsLocation() {
  return new Promise((resolve, reject) => {
    if (!navigator.geolocation) {
      reject(new Error('Geolocation is not supported by this browser'));
      return;
    }
    navigator.geolocation.getCurrentPosition(
      pos => resolve({
        latitude: Math.round(pos.coords.latitude * 10000) / 10000,
        longitude: Math.round(pos.coords.longitude * 10000) / 10000,
      }),
      err => reject(new Error(err.message || 'Could not detect location')),
      { enableHighAccuracy: true, timeout: 12000 }
    );
  });
}

export function buildLocationLabel(region) {
  const parts = [region.city, region.state, region.country].filter(Boolean);
  if (parts.length) return parts.join(', ');
  if (region.latitude != null) {
    return `${region.latitude.toFixed(2)}°, ${region.longitude.toFixed(2)}°`;
  }
  return 'Custom coordinates';
}
