import { useEffect, useState } from "react";
import { Download, FileOutput } from "lucide-react";
import Markdown from "../components/Markdown";
import { api, download } from "../lib/api";
import { useToast } from "../contexts/ToastContext";

export default function DocumentsPage() {
  const [repos, setRepos] = useState([]);
  const [projects, setProjects] = useState([]);
  const [selected, setSelected] = useState("");
  const [preview, setPreview] = useState("");
  const toast = useToast();
  useEffect(() => { Promise.all([api("/repositories"), api("/agents/projects")]).then(([r, p]) => { setRepos(r.filter((repo) => repo.status === "ready")); setProjects(p); }); }, []);
  async function view() {
    try { const analysis = await api(`/analysis/${selected}`); setPreview(analysis.architecture_report); } catch (error) { toast(error.message, "error"); }
  }
  return (
    <div className="space-y-6">
      <div><p className="label">Knowledge center</p><h1 className="text-3xl font-semibold">Documentation viewer</h1></div>
      <section className="panel">
        <h2 className="mb-4 flex items-center gap-2 font-semibold"><FileOutput size={18} /> Repository architecture documents</h2>
        <div className="flex flex-col gap-3 sm:flex-row"><select className="input" value={selected} onChange={(e) => setSelected(e.target.value)}><option value="">Select repository</option>{repos.map((repo) => <option value={repo.id} key={repo.id}>{repo.name}</option>)}</select><button disabled={!selected} className="button-secondary" onClick={view}>Preview</button><button disabled={!selected} className="button-primary" onClick={() => download(`/documents/repository/${selected}/pdf`, "architecture-report.pdf").catch((error) => toast(error.message, "error"))}><Download size={16} /> Export PDF</button></div>
        {preview && <div className="mt-7 rounded-xl bg-slate-100 p-5 dark:bg-white/[.03]"><Markdown>{preview}</Markdown></div>}
      </section>
      <section className="panel">
        <h2 className="mb-4 font-semibold">Generated project bundles</h2>
        <div className="space-y-3">{projects.map((project) => <div key={project.id} className="flex flex-col justify-between gap-3 rounded-xl border border-slate-100 p-4 dark:border-white/5 sm:flex-row sm:items-center"><div><p className="font-medium">{project.name}</p><p className="text-sm text-slate-500">Plan, backend, frontend, docs, and review output</p></div><button className="button-secondary" onClick={() => download(`/documents/project/${project.id}/zip`, `${project.name}.zip`).catch((error) => toast(error.message, "error"))}><Download size={15} /> Download ZIP</button></div>)}{!projects.length && <p className="text-sm text-slate-500">Agent-generated documentation bundles will be listed here.</p>}</div>
      </section>
    </div>
  );
}

