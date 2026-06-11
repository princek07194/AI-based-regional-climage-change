import { Loader2 } from 'lucide-react';

export default function LoadingOverlay({ message = 'Analysing regional weather patterns…' }) {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/70 backdrop-blur-sm">
      <div className="glass-strong rounded-2xl px-10 py-8 text-center animate-pulse-soft">
        <Loader2 className="w-12 h-12 text-sky-400 animate-spin mx-auto mb-4" />
        <p className="text-white font-semibold">{message}</p>
        <p className="text-slate-400 text-sm mt-2">Running XGBoost + SHAP</p>
      </div>
    </div>
  );
}
