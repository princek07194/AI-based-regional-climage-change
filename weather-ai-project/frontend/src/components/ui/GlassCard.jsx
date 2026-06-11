export default function GlassCard({ children, className = '' }) {
  return (
    <div className={`rounded-2xl glass p-6 animate-fadeIn ${className}`}>
      {children}
    </div>
  );
}
