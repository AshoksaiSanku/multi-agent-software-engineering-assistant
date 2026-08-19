import { useEffect, useState } from "react";
import { FolderSearch, Github, Search, Trash2, X } from "lucide-react";
import { api } from "../lib/api";
import { Loader, Status } from "../components/Ui";
import { useToast } from "../contexts/ToastContext";

export default function RepositoriesPage() {
  const [repos, setRepos] = useState([]);
  const [form, setForm] = useState({ name: "", github_url: "" });
  const [selected, setSelected] = useState("");
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [deletingId, setDeletingId] = useState("");
  const [repositoryToDelete, setRepositoryToDelete] = useState(null);
  const toast = useToast();
  const load = () => api("/repositories").then(setRepos);
  useEffect(() => { load(); }, []);
  async function add(event) {
    event.preventDefault(); setLoading(true);
    try { await api("/repositories", { method: "POST", body: JSON.stringify(form) }); setForm({ name: "", github_url: "" }); await load(); toast("Repository ingestion queued"); }
    catch (error) { toast(error.message, "error"); } finally { setLoading(false); }
  }
  async function search(event) {
    event.preventDefault();
    try { setResults(await api(`/repositories/${selected}/search`, { method: "POST", body: JSON.stringify({ query }) })); }
    catch (error) { toast(error.message, "error"); }
  }
  async function removeRepository() {
    const repo = repositoryToDelete;
    if (!repo) return;
    const previousRepos = repos;
    setDeletingId(repo.id);
    setRepositoryToDelete(null);
    setRepos((items) => items.filter((item) => item.id !== repo.id));
    if (selected === repo.id) {
      setSelected("");
      setResults([]);
    }
    try {
      await api(`/repositories/${repo.id}`, { method: "DELETE" });
      toast("Repository removed successfully");
    } catch (error) {
      setRepos(previousRepos);
      toast(error.message, "error");
    } finally {
      setDeletingId("");
    }
  }
  return (
    <div className="space-y-6">
      <div><p className="label">Repository intelligence</p><h1 className="text-3xl font-semibold">GitHub ingestion and semantic search</h1></div>
      <div className="grid gap-5 lg:grid-cols-[.8fr_1.2fr]">
        <form className="panel space-y-4" onSubmit={add}>
          <h2 className="flex items-center gap-2 font-semibold"><Github size={19} /> Connect repository</h2>
          <div><label className="label">Display name</label><input required className="input" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} placeholder="Payments API" /></div>
          <div><label className="label">Public GitHub URL</label><input required type="url" className="input" value={form.github_url} onChange={(e) => setForm({ ...form, github_url: e.target.value })} placeholder="https://github.com/org/repository" /></div>
          <button disabled={loading} className="button-primary w-full">{loading ? <Loader label="Queuing" /> : "Index repository"}</button>
        </form>
        <div className="panel">
          <h2 className="mb-4 font-semibold">Connected repositories</h2>
          <div className="space-y-3">{repos.map((repo) => <div key={repo.id} className={`flex w-full items-center gap-3 rounded-xl border p-3 transition ${selected === repo.id ? "border-accent/50 bg-accent/5" : "border-slate-100 dark:border-white/5"}`}><button type="button" onClick={() => setSelected(repo.id)} className="flex flex-1 items-center justify-between gap-3 text-left"><div><p className="font-medium">{repo.name}</p><p className="text-xs text-slate-500">{repo.file_count} files / {repo.default_branch || "pending branch"}</p></div><Status value={repo.status} /></button><button type="button" disabled={deletingId === repo.id} onClick={() => setRepositoryToDelete(repo)} className="rounded-xl border border-red-500/20 p-2 text-red-400 transition hover:bg-red-500/10 disabled:cursor-not-allowed disabled:opacity-50" title="Delete repository"><Trash2 size={17} /></button></div>)}</div>
        </div>
      </div>
      <form onSubmit={search} className="panel">
        <h2 className="mb-4 flex items-center gap-2 font-semibold"><FolderSearch size={18} /> Semantic code search</h2>
        <div className="flex flex-col gap-3 sm:flex-row"><select className="input sm:max-w-xs" required value={selected} onChange={(e) => setSelected(e.target.value)}><option value="">Select repository</option>{repos.filter((repo) => repo.status === "ready").map((repo) => <option key={repo.id} value={repo.id}>{repo.name}</option>)}</select><input className="input" required value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Where is authentication enforced?" /><button className="button-primary"><Search size={16} /> Search</button></div>
        <div className="mt-5 space-y-3">{results.map((result) => <div key={`${result.file_path}-${result.score}`} className="rounded-xl bg-slate-100 p-4 dark:bg-white/[.03]"><p className="mb-2 text-sm font-medium text-accent">{result.file_path} <span className="ml-2 text-xs text-slate-500">{result.score > 0 ? `${Math.round(result.score * 100)}% match` : "context result"}</span></p><pre className="overflow-hidden whitespace-pre-wrap text-xs text-slate-500">{result.content.slice(0, 380)}</pre></div>)}</div>
      </form>
      {repositoryToDelete && <div className="fixed inset-0 z-50 flex items-center justify-center bg-ink/60 p-4 backdrop-blur-sm"><div className="panel w-full max-w-md shadow-glow"><div className="mb-4 flex items-center justify-between"><h2 className="text-lg font-semibold">Remove repository</h2><button type="button" onClick={() => setRepositoryToDelete(null)} className="rounded-lg p-1 text-slate-400 hover:bg-slate-100 dark:hover:bg-white/10"><X size={18} /></button></div><p className="text-sm text-slate-500">Are you sure you want to remove this repository?</p><p className="mt-3 rounded-xl bg-slate-100 p-3 text-sm font-medium dark:bg-white/[.04]">{repositoryToDelete.name}</p><div className="mt-6 flex justify-end gap-3"><button type="button" className="button-secondary" onClick={() => setRepositoryToDelete(null)}>Cancel</button><button type="button" className="button-primary !bg-red-500 hover:!bg-red-400" onClick={removeRepository}>Delete repository</button></div></div></div>}
    </div>
  );
}
