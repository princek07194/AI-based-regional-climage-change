export default function InputSlider({ label, icon: Icon, name, value, onChange, min, max, step = 1, unit }) {
  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between">
        <label className="flex items-center gap-2 text-sm font-medium text-slate-300">
          <Icon className="w-4 h-4 text-sky-400" />
          {label}
        </label>
        <span className="text-sky-300 font-bold text-sm">{value}{unit}</span>
      </div>
      <input
        type="range"
        name={name}
        min={min}
        max={max}
        step={step}
        value={value}
        onChange={onChange}
        className="w-full h-2 rounded-full appearance-none cursor-pointer bg-slate-700 accent-sky-400"
      />
      <div className="flex justify-between text-xs text-slate-500">
        <span>{min}{unit}</span>
        <span>{max}{unit}</span>
      </div>
    </div>
  );
}
