import { useEffect, useState } from "react";
import { Activity, ArrowRight } from "lucide-react";
import { Link } from "react-router-dom";
import { api } from "../lib/api";
import { MetricCard, Status } from "../components/Ui";

export default function DashboardPage() {
  const [repos, setRepos] = useState([]);
  const [logs, setLogs] = useState([]);
  const [predictions, setPredictions] = useState([]);
  useEffect(() => {
    Promise.all([api("/repositories"), api("/agents/logs"), api("/ml/predictions")]).then(([r, l, p]) => {
      setRepos(r); setLogs(l); setPredictions(p);
    });
  }, []);
  const averageRisk = predictions.length ? Math.round(predictions.reduce((sum, value) => sum + value.bug_probability, 0) / predictions.length * 100) : 0;
  return (
    <div className="space-y-7">
      <div><p className="label">Command center</p><h1 className="text-3xl font-semibold">Engineering overview</h1><p className="mt-2 text-slate-500">Repository intelligence and active agent work in one view.</p></div>
      <section className="grid gap-4 md:grid-cols-3">
        <MetricCard title="Repositories" value={repos.length} detail={`${repos.filter((repo) => repo.status === "ready").length} ready for RAG`} />
        <MetricCard title="Agent Events" value={logs.length} detail="Recorded workflow actions" />
        <MetricCard title="Average Bug Risk" value={`${averageRisk}%`} detail={`${predictions.length} evaluated files`} />
      </section>
      <section className="grid gap-5 lg:grid-cols-[1.2fr_.8fr]">
        <div className="panel">
          <div className="mb-5 flex items-center justify-between"><h2 className="font-semibold">Repositories</h2><Link className="text-sm text-accent" to="/repositories">Add repository <ArrowRight className="inline" size={14} /></Link></div>
          <div className="space-y-3">{repos.slice(0, 5).map((repo) => <div key={repo.id} className="flex items-center justify-between rounded-xl border border-slate-100 p-4 dark:border-white/5"><div><p className="font-medium">{repo.name}</p><p className="text-xs text-slate-500">{repo.file_count} source files indexed</p></div><Status value={repo.status} /></div>)}{!repos.length && <p className="text-sm text-slate-500">Upload a GitHub URL to start repository intelligence.</p>}</div>
        </div>
        <div className="panel">
          <h2 className="mb-5 flex items-center gap-2 font-semibold"><Activity size={17} className="text-aqua" /> Recent agent activity</h2>
          <div className="space-y-4">{logs.slice(0, 6).map((log) => <div key={log.id}><div className="flex justify-between gap-3 text-sm"><span>{log.agent_name}</span><Status value={log.status} /></div><p className="mt-1 text-xs text-slate-500">{log.message}</p></div>)}{!logs.length && <p className="text-sm text-slate-500">Agent runs will appear here.</p>}</div>
        </div>
      </section>
    </div>
  );
}

