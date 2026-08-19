import { useEffect, useState } from "react";
import { Gauge, ShieldAlert } from "lucide-react";
import { Loader } from "../components/Ui";
import { api } from "../lib/api";
import { useToast } from "../contexts/ToastContext";

const defaultMetrics = { cyclomatic_complexity: 12, file_size: 340, dependency_count: 6, commit_frequency: 8 };

export default function MLPage() {
  const [repos, setRepos] = useState([]);
  const [predictions, setPredictions] = useState([]);
  const [form, setForm] = useState({ repository_id: "", file_path: "src/module.py", metrics: defaultMetrics });
  const [availableFiles, setAvailableFiles] = useState([]);
  const [estimating, setEstimating] = useState(false);
  const toast = useToast();
  useEffect(() => { Promise.all([api("/repositories"), api("/ml/predictions")]).then(([r, p]) => { setRepos(r); setPredictions(p); }); }, []);

  async function loadRepositoryEstimate(repositoryId, filePath = "") {
    if (!repositoryId) {
      setAvailableFiles([]);
      setForm({ repository_id: "", file_path: "src/module.py", metrics: defaultMetrics });
      return;
    }
    setEstimating(true);
    try {
      const query = filePath ? `?file_path=${encodeURIComponent(filePath)}` : "";
      const estimate = await api(`/ml/repositories/${repositoryId}/estimate${query}`);
      setAvailableFiles(estimate.available_files || []);
      setForm({ repository_id: repositoryId, file_path: estimate.file_path, metrics: estimate.metrics });
      toast("Repository metrics loaded");
    } catch (error) {
      toast(error.message, "error");
      setForm((current) => ({ ...current, repository_id: repositoryId }));
    } finally {
      setEstimating(false);
    }
  }

  async function assess(event) {
    event.preventDefault();
    try {
      const output = await api("/ml/predict", { method: "POST", body: JSON.stringify({ ...form, repository_id: form.repository_id || null }) });
      setPredictions((items) => [output, ...items]); toast("Risk score calculated");
    } catch (error) { toast(error.message, "error"); }
  }
  return (
    <div className="space-y-6">
      <div><p className="label">Predictive engineering</p><h1 className="text-3xl font-semibold">ML bug-risk scoring</h1><p className="mt-2 text-slate-500">XGBoost classifies risk while a regression model scores maintainability.</p></div>
      <div className="grid gap-5 lg:grid-cols-[.8fr_1.2fr]">
        <form onSubmit={assess} className="panel space-y-4">
          <select className="input" value={form.repository_id} onChange={(e) => loadRepositoryEstimate(e.target.value)}><option value="">No linked repository</option>{repos.filter((repo) => repo.status === "ready").map((repo) => <option key={repo.id} value={repo.id}>{repo.name}</option>)}</select>
          {availableFiles.length > 0 && <div><label className="label">Repository file</label><select className="input" value={form.file_path} onChange={(e) => loadRepositoryEstimate(form.repository_id, e.target.value)}>{availableFiles.map((file) => <option key={file} value={file}>{file}</option>)}</select></div>}
          <div><label className="label">File path</label><input required className="input" value={form.file_path} onChange={(e) => setForm({ ...form, file_path: e.target.value })} /></div>
          {estimating && <div className="rounded-xl bg-slate-100 p-3 dark:bg-white/[.04]"><Loader label="Estimating repository metrics" /></div>}
          {Object.entries(form.metrics).map(([key, value]) => <div key={key}><label className="label">{key.replaceAll("_", " ")}</label><input type="number" min="0" className="input" value={value} onChange={(e) => setForm({ ...form, metrics: { ...form.metrics, [key]: Number(e.target.value) } })} /></div>)}
          <button disabled={estimating} className="button-primary w-full"><Gauge size={16} /> Predict quality</button>
        </form>
        <div className="panel">
          <h2 className="mb-4 flex items-center gap-2 font-semibold"><ShieldAlert size={18} className="text-amber-400" /> Predictions</h2>
          <div className="space-y-4">{predictions.map((prediction) => { const repo = repos.find((item) => item.id === prediction.repository_id); return <div className="rounded-xl border border-slate-100 p-4 dark:border-white/5" key={prediction.id}><div className="flex items-center justify-between gap-3"><div><p className="font-medium">{prediction.file_path}</p>{repo && <p className="text-xs text-slate-500">{repo.name}</p>}</div><span className={`text-sm font-semibold ${prediction.bug_probability > 0.65 ? "text-red-400" : "text-aqua"}`}>{Math.round(prediction.bug_probability * 100)}% risk</span></div><div className="my-3 h-2 rounded bg-slate-200 dark:bg-white/10"><div className="h-2 rounded bg-accent" style={{ width: `${prediction.maintainability_score}%` }} /></div><p className="text-xs text-slate-500">Maintainability {prediction.maintainability_score}/100</p><ul className="mt-3 space-y-1 text-sm text-slate-500">{prediction.recommendations.map((recommendation) => <li key={recommendation}>- {recommendation}</li>)}</ul></div>; })}</div>
        </div>
      </div>
    </div>
  );
}
