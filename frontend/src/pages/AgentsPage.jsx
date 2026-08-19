import { useEffect, useState } from "react";
import { Download, Play, Radio, Trash2, X } from "lucide-react";
import { Loader, Status } from "../components/Ui";
import { useAuth } from "../contexts/AuthContext";
import { useToast } from "../contexts/ToastContext";
import { api, download, token, WS_URL } from "../lib/api";

export default function AgentsPage() {
  const { user } = useAuth();
  const toast = useToast();
  const [repos, setRepos] = useState([]);
  const [logs, setLogs] = useState([]);
  const [projects, setProjects] = useState([]);
  const [running, setRunning] = useState(false);
  const [deletingProjectId, setDeletingProjectId] = useState("");
  const [projectToDelete, setProjectToDelete] = useState(null);
  const [form, setForm] = useState({ repository_id: "", project_name: "", requirements: "" });
  useEffect(() => {
    Promise.all([api("/repositories"), api("/agents/logs"), api("/agents/projects")]).then(([r, l, p]) => { setRepos(r); setLogs(l); setProjects(p); });
  }, []);
  useEffect(() => {
    const channel = form.repository_id || user.id;
    const socket = new WebSocket(`${WS_URL}/agents/ws/${channel}?token=${encodeURIComponent(token())}`);
    socket.onmessage = (event) => {
      const incoming = JSON.parse(event.data);
      setLogs((items) => [{ ...incoming, id: `${incoming.run_id}-${incoming.agent_name}-${Date.now()}` }, ...items]);
      if (incoming.agent_name === "Orchestrator" && incoming.status === "completed") {
        setRunning(false);
        api("/agents/projects").then(setProjects);
      }
    };
    return () => socket.close();
  }, [form.repository_id, user.id]);
  async function launch(event) {
    event.preventDefault(); setRunning(true);
    try {
      const response = await api("/agents/runs", { method: "POST", body: JSON.stringify({ ...form, repository_id: form.repository_id || null }) });
      toast(`Agent run ${response.run_id.slice(0, 8)} queued`);
    } catch (error) { setRunning(false); toast(error.message, "error"); }
  }
  async function removeProject() {
    const project = projectToDelete;
    if (!project) return;
    const previousProjects = projects;
    setDeletingProjectId(project.id);
    setProjectToDelete(null);
    setProjects((items) => items.filter((item) => item.id !== project.id));
    try {
      await api(`/agents/projects/${project.id}`, { method: "DELETE" });
      toast("Generated project deleted successfully");
    } catch (error) {
      setProjects(previousProjects);
      toast(error.message, "error");
    } finally {
      setDeletingProjectId("");
    }
  }
  return (
    <div className="space-y-6">
      <div><p className="label">Orchestration</p><h1 className="text-3xl font-semibold">AI engineering team</h1><p className="mt-2 text-slate-500">Six specialist agents plan, build, document, and review your requested feature.</p></div>
      <div className="grid gap-5 xl:grid-cols-[.8fr_1.2fr]">
        <form className="panel space-y-4" onSubmit={launch}>
          <h2 className="font-semibold">Launch new project generation</h2>
          <div><label className="label">Project name</label><input required className="input" value={form.project_name} onChange={(e) => setForm({ ...form, project_name: e.target.value })} /></div>
          <div><label className="label">Repository context</label><select className="input" value={form.repository_id} onChange={(e) => setForm({ ...form, repository_id: e.target.value })}><option value="">New standalone project</option>{repos.filter((repo) => repo.status === "ready").map((repo) => <option key={repo.id} value={repo.id}>{repo.name}</option>)}</select></div>
          <div><label className="label">Requirements</label><textarea required minLength={10} rows={8} className="input resize-none" value={form.requirements} onChange={(e) => setForm({ ...form, requirements: e.target.value })} placeholder="Build a secure notification API with a React settings page..." /></div>
          <button className="button-primary w-full" disabled={running}>{running ? <Loader label="Agents collaborating" /> : <><Play size={16} /> Start agents</>}</button>
        </form>
        <div className="panel">
          <div className="mb-5 flex items-center justify-between"><h2 className="flex items-center gap-2 font-semibold"><Radio size={17} className="text-aqua" /> Live activity</h2>{running && <Status value="running" />}</div>
          <div className="max-h-[34rem] space-y-3 overflow-y-auto">{logs.map((log) => <div key={log.id} className="rounded-xl border border-slate-100 p-4 dark:border-white/5"><div className="flex justify-between gap-3"><p className="text-sm font-medium">{log.agent_name}</p><Status value={log.status} /></div><p className="mt-2 text-xs text-slate-500">{log.message}</p></div>)}{!logs.length && <p className="text-sm text-slate-500">Start a run to stream agent decisions here.</p>}</div>
        </div>
      </div>
      <section className="panel">
        <h2 className="mb-4 font-semibold">Generated deliverables</h2>
        <div className="grid gap-3 md:grid-cols-2">{projects.map((project) => <div key={project.id} className="flex items-center justify-between gap-3 rounded-xl bg-slate-100 p-4 dark:bg-white/[.03]"><div><p className="font-medium">{project.name}</p><p className="text-xs text-slate-500">{Object.keys(project.files).length} generated artifacts</p></div><div className="flex items-center gap-2"><button className="button-secondary !py-2" onClick={() => download(`/documents/project/${project.id}/zip`, `${project.name}.zip`).catch((error) => toast(error.message, "error"))}><Download size={15} /> ZIP</button><button type="button" disabled={deletingProjectId === project.id} onClick={() => setProjectToDelete(project)} className="rounded-xl border border-red-500/20 p-2.5 text-red-400 transition hover:bg-red-500/10 disabled:cursor-not-allowed disabled:opacity-50" title="Delete generated project"><Trash2 size={16} /></button></div></div>)}</div>
      </section>
      {projectToDelete && <div className="fixed inset-0 z-50 flex items-center justify-center bg-ink/60 p-4 backdrop-blur-sm"><div className="panel w-full max-w-md shadow-glow"><div className="mb-4 flex items-center justify-between"><h2 className="text-lg font-semibold">Delete generated project</h2><button type="button" onClick={() => setProjectToDelete(null)} className="rounded-lg p-1 text-slate-400 hover:bg-slate-100 dark:hover:bg-white/10"><X size={18} /></button></div><p className="text-sm text-slate-500">Are you sure you want to delete this generated project?</p><p className="mt-3 rounded-xl bg-slate-100 p-3 text-sm font-medium dark:bg-white/[.04]">{projectToDelete.name}</p><div className="mt-6 flex justify-end gap-3"><button type="button" className="button-secondary" onClick={() => setProjectToDelete(null)}>Cancel</button><button type="button" className="button-primary !bg-red-500 hover:!bg-red-400" onClick={removeProject}>Delete project</button></div></div></div>}
    </div>
  );
}
