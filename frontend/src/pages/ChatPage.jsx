import { useEffect, useState } from "react";
import { SendHorizontal } from "lucide-react";
import Markdown from "../components/Markdown";
import { Loader } from "../components/Ui";
import { api } from "../lib/api";
import { useToast } from "../contexts/ToastContext";

export default function ChatPage() {
  const [repos, setRepos] = useState([]);
  const [repositoryId, setRepositoryId] = useState("");
  const [messages, setMessages] = useState([]);
  const [question, setQuestion] = useState("");
  const [waiting, setWaiting] = useState(false);
  const toast = useToast();
  useEffect(() => { api("/repositories").then((items) => setRepos(items.filter((repo) => repo.status === "ready"))); }, []);
  useEffect(() => { api(`/chat/history${repositoryId ? `?repository_id=${repositoryId}` : ""}`).then(setMessages); }, [repositoryId]);
  async function submit(event) {
    event.preventDefault();
    const value = question; setQuestion(""); setWaiting(true);
    setMessages((current) => [...current, { id: Date.now(), role: "user", content: value }]);
    try {
      const result = await api("/chat", { method: "POST", body: JSON.stringify({ repository_id: repositoryId || null, question: value }) });
      setMessages((current) => [...current, { id: `${Date.now()}-a`, role: "assistant", content: result.answer }]);
    } catch (error) { toast(error.message, "error"); } finally { setWaiting(false); }
  }
  return (
    <div className="flex h-[calc(100vh-8.5rem)] flex-col gap-5">
      <div className="flex flex-col justify-between gap-3 sm:flex-row sm:items-end"><div><p className="label">RAG assistant</p><h1 className="text-3xl font-semibold">Repository chat</h1></div><select className="input sm:max-w-xs" value={repositoryId} onChange={(e) => setRepositoryId(e.target.value)}><option value="">General assistant</option>{repos.map((repo) => <option value={repo.id} key={repo.id}>{repo.name}</option>)}</select></div>
      <section className="panel flex-1 space-y-5 overflow-y-auto">
        {!messages.length && <div className="mx-auto mt-16 max-w-lg text-center text-slate-500">Ask how a feature works, locate an API boundary, or request a secure implementation suggestion.</div>}
        {messages.map((message) => <div key={message.id} className={`max-w-3xl rounded-2xl p-4 ${message.role === "user" ? "ml-auto bg-accent text-white" : "bg-slate-100 dark:bg-white/[.04]"}`}>{message.role === "assistant" ? <Markdown>{message.content}</Markdown> : message.content}</div>)}
        {waiting && <Loader label="Agents are reading context" />}
      </section>
      <form onSubmit={submit} className="flex gap-3"><input className="input flex-1" required value={question} onChange={(e) => setQuestion(e.target.value)} placeholder="Ask a question about the repository..." /><button disabled={waiting} className="button-primary"><SendHorizontal size={17} /> Send</button></form>
    </div>
  );
}

