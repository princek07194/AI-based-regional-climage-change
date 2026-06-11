/** Offline fallback when /api/regions is unavailable */
export const FALLBACK_COUNTRIES = [
  {
    name: 'India',
    states: [
      {
        name: 'Jammu and Kashmir',
        cities: [
          { name: 'Srinagar', latitude: 34.08, longitude: 74.8, climate_zone: 'Alpine / Himalayan' },
          { name: 'Leh', latitude: 34.15, longitude: 77.58, climate_zone: 'Alpine / Himalayan' },
        ],
      },
      {
        name: 'Rajasthan',
        cities: [
          { name: 'Jaipur', latitude: 26.91, longitude: 75.79, climate_zone: 'Subtropical' },
          { name: 'Jodhpur', latitude: 26.24, longitude: 73.02, climate_zone: 'Subtropical' },
        ],
      },
      {
        name: 'Delhi',
        cities: [{ name: 'New Delhi', latitude: 28.61, longitude: 77.21, climate_zone: 'Subtropical' }],
      },
      {
        name: 'Punjab',
        cities: [
          { name: 'Amritsar', latitude: 31.63, longitude: 74.87, climate_zone: 'Subtropical' },
          { name: 'Chandigarh', latitude: 30.74, longitude: 76.79, climate_zone: 'Subtropical' },
        ],
      },
      {
        name: 'Uttar Pradesh',
        cities: [
          { name: 'Lucknow', latitude: 26.85, longitude: 80.95, climate_zone: 'Humid Subtropical' },
          { name: 'Varanasi', latitude: 25.32, longitude: 82.99, climate_zone: 'Humid Subtropical' },
        ],
      },
      {
        name: 'Bihar',
        cities: [
          { name: 'Patna', latitude: 25.61, longitude: 85.14, climate_zone: 'Humid Subtropical' },
          { name: 'Gaya', latitude: 24.79, longitude: 84.99, climate_zone: 'Humid Subtropical' },
        ],
      },
      {
        name: 'Maharashtra',
        cities: [{ name: 'Mumbai', latitude: 19.08, longitude: 72.88, climate_zone: 'Tropical Wet & Dry' }],
      },
    ],
  },
];
