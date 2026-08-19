import { useState } from "react";
import { BrainCircuit, Sparkles } from "lucide-react";
import { useAuth } from "../contexts/AuthContext";
import { useToast } from "../contexts/ToastContext";
import { Loader } from "../components/Ui";

export default function LoginPage() {
  const [registering, setRegistering] = useState(false);
  const [form, setForm] = useState({ email: "", password: "", full_name: "" });
  const [loading, setLoading] = useState(false);
  const auth = useAuth();
  const toast = useToast();
  async function submit(event) {
    event.preventDefault();
    setLoading(true);
    try {
      await (registering ? auth.register(form) : auth.login(form));
      toast(registering ? "Account created" : "Welcome back");
    } catch (error) {
      toast(error.message, "error");
    } finally {
      setLoading(false);
    }
  }
  return (
    <div className="ambient grid min-h-screen bg-ink lg:grid-cols-2">
      <section className="hidden flex-col justify-between p-14 text-white lg:flex">
        <div className="flex items-center gap-3"><BrainCircuit className="text-aqua" /> <span className="text-lg font-semibold">DevAgents</span></div>
        <div className="max-w-xl">
          <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-aqua/20 bg-aqua/10 px-4 py-2 text-sm text-aqua"><Sparkles size={15} /> AI engineering workspace</div>
          <h1 className="text-5xl font-semibold leading-tight">Ship software with an entire AI engineering team.</h1>
          <p className="mt-6 text-lg text-slate-400">Understand repositories, generate implementations, inspect risk, and publish docs from one secure workspace.</p>
        </div>
        <p className="text-sm text-slate-500">LangGraph orchestration / Chroma RAG / XGBoost risk modeling</p>
      </section>
      <section className="flex items-center justify-center p-5">
        <form onSubmit={submit} className="panel w-full max-w-md !border-white/10 !bg-panel !p-8 text-slate-100 shadow-glow">
          <h2 className="text-2xl font-semibold">{registering ? "Create account" : "Sign in"}</h2>
          <p className="mb-8 mt-2 text-sm text-slate-400">Access your engineering command center.</p>
          {registering && <div className="mb-5"><label className="label">Full name</label><input className="input" required value={form.full_name} onChange={(e) => setForm({ ...form, full_name: e.target.value })} /></div>}
          <div className="mb-5"><label className="label">Email</label><input type="email" className="input" required value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} /></div>
          <div className="mb-7"><label className="label">Password</label><input type="password" minLength={8} className="input" required value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} /></div>
          <button disabled={loading} className="button-primary w-full">{loading ? <Loader label="Authenticating" /> : registering ? "Start building" : "Sign in"}</button>
          <button type="button" className="mt-6 w-full text-sm text-slate-400 hover:text-white" onClick={() => setRegistering(!registering)}>
            {registering ? "Already registered? Sign in" : "New here? Create an account"}
          </button>
        </form>
      </section>
    </div>
  );
}

