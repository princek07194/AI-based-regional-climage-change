/** Map weather condition label → emoji icon for UI cards. */
const ICON_MAP = [
  { keys: ['sunny', 'clear'], icon: '☀️' },
  { keys: ['partly cloudy', 'cloudy', 'overcast'], icon: '⛅' },
  { keys: ['mist', 'fog', 'freezing fog'], icon: '🌫️' },
  { keys: ['snow', 'blizzard', 'blowing snow', 'sleet', 'ice pellet'], icon: '❄️' },
  { keys: ['thunder', 'thundery'], icon: '⛈️' },
  { keys: ['heavy rain', 'torrential', 'moderate rain'], icon: '🌧️' },
  { keys: ['rain', 'drizzle', 'shower'], icon: '🌦️' },
];

export function getWeatherIcon(condition = '') {
  const lower = condition.toLowerCase();
  for (const { keys, icon } of ICON_MAP) {
    if (keys.some(k => lower.includes(k))) return icon;
  }
  return '🌤️';
}

export const RISK_COLORS = {
  Low: '#22c55e',
  Moderate: '#eab308',
  High: '#f97316',
  Severe: '#ef4444',
};

export const BAR_POS = '#38bdf8';
export const BAR_NEG = '#f87171';
