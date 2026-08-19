import { useEffect, useState } from "react";
import { ScanSearch } from "lucide-react";
import Markdown from "../components/Markdown";
import { Loader, MetricCard } from "../components/Ui";
import { api } from "../lib/api";
import { useToast } from "../contexts/ToastContext";

export default function AnalysisPage() {
  const [repos, setRepos] = useState([]);
  const [selected, setSelected] = useState("");
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);
  const toast = useToast();
  useEffect(() => { api("/repositories").then((values) => setRepos(values.filter((value) => value.status === "ready"))); }, []);
  async function analyze() {
    setLoading(true);
    try { setReport(await api(`/analysis/${selected}`)); } catch (error) { toast(error.message, "error"); } finally { setLoading(false); }
  }
  const summary = report?.summary || {};
  return (
    <div className="space-y-6">
      <div><p className="label">Architecture intelligence</p><h1 className="text-3xl font-semibold">Code analysis dashboard</h1></div>
      <div className="panel flex flex-col gap-3 sm:flex-row"><select className="input" value={selected} onChange={(e) => setSelected(e.target.value)}><option value="">Choose an indexed repository</option>{repos.map((repo) => <option key={repo.id} value={repo.id}>{repo.name}</option>)}</select><button disabled={!selected || loading} className="button-primary sm:min-w-48" onClick={analyze}>{loading ? <Loader label="Analyzing" /> : <><ScanSearch size={16} /> Generate analysis</>}</button></div>
      {report && <>
        <div className="grid gap-4 md:grid-cols-3"><MetricCard title="Source Lines" value={summary.total_lines || 0} detail="Indexed code footprint" /><MetricCard title="Files" value={Object.values(summary.languages || {}).reduce((a, b) => a + b, 0)} detail="Parsed file set" /><MetricCard title="API Markers" value={summary.api_route_markers || 0} detail="Detected route decorators" /></div>
        <article className="panel"><h2 className="mb-5 font-semibold">Architecture report</h2><Markdown>{report.architecture_report}</Markdown></article>
      </>}
    </div>
  );
}

