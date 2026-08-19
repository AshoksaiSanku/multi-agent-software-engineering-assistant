import { LoaderCircle } from "lucide-react";

export function Loader({ label = "Thinking" }) {
  return <span className="inline-flex items-center gap-2 text-sm text-slate-400"><LoaderCircle className="animate-spin" size={16} />{label}</span>;
}

export function Status({ value }) {
  const tones = { ready: "bg-emerald-500/10 text-emerald-400", completed: "bg-emerald-500/10 text-emerald-400", failed: "bg-red-500/10 text-red-400", indexing: "bg-amber-500/10 text-amber-400", running: "bg-violet-500/10 text-violet-400", queued: "bg-slate-500/10 text-slate-400" };
  return <span className={`rounded-full px-2.5 py-1 text-xs font-medium capitalize ${tones[value] || tones.queued}`}>{value}</span>;
}

export function MetricCard({ title, value, detail }) {
  return <div className="panel"><p className="text-xs uppercase tracking-[0.17em] text-slate-500">{title}</p><p className="mt-3 text-3xl font-semibold">{value}</p><p className="mt-2 text-sm text-slate-500">{detail}</p></div>;
}

