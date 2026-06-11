/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        sky: {
          950: '#0c1a2e',
        }
      }
    }
  },
  plugins: [],
}
