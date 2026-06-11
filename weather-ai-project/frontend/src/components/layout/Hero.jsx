import { Zap, Brain, Globe, Award } from 'lucide-react';

export default function Hero() {
  return (
    <header className="relative overflow-hidden">
      <div className="absolute inset-0 weather-bg-animate opacity-30 pointer-events-none" />
      <div className="absolute top-0 left-1/4 w-96 h-96 rounded-full opacity-10 blur-3xl"
        style={{ background: 'radial-gradient(circle,#38bdf8,transparent)' }} />
      <div className="absolute top-0 right-1/4 w-80 h-80 rounded-full opacity-10 blur-3xl"
        style={{ background: 'radial-gradient(circle,#818cf8,transparent)' }} />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 py-16 text-center relative z-10">
        <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full mb-6
          bg-sky-500/10 border border-sky-500/30 text-sky-400 text-sm font-medium">
          <Zap className="w-4 h-4" /> Region-Aware XGBoost + SHAP Explainable AI
        </div>
        <h1 className="text-5xl sm:text-6xl font-black text-white mb-4 tracking-tight">
          RegionalClimate <span className="text-transparent bg-clip-text"
            style={{ backgroundImage: 'linear-gradient(90deg,#38bdf8,#818cf8)' }}>XAI</span>
        </h1>
        <p className="text-slate-400 text-lg max-w-2xl mx-auto">
          Region-aware explainable weather prediction — latitude, longitude, and climate context
          shape every forecast with full SHAP transparency.
        </p>
        <div className="flex flex-wrap justify-center gap-6 mt-10">
          {[
            { icon: Brain, label: 'XGBoost Model', value: '48-class' },
            { icon: Globe, label: 'Region Features', value: 'Lat/Lon' },
            { icon: Award, label: 'Explainability', value: 'SHAP XAI' },
          ].map(({ icon: Icon, label, value }) => (
            <div key={label} className="glass rounded-xl px-5 py-3 flex items-center gap-3">
              <Icon className="w-5 h-5 text-sky-400" />
              <div className="text-left">
                <div className="text-white font-bold text-sm">{value}</div>
                <div className="text-slate-400 text-xs">{label}</div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </header>
  );
}
