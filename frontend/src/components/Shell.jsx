import { Bot, BrainCircuit, ChartNoAxesColumn, Code2, FileText, FolderGit2, LayoutDashboard, LogOut, Moon, Sun } from "lucide-react";
import { createElement } from "react";
import { NavLink, Outlet } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import { useTheme } from "../contexts/ThemeContext";

const navigation = [
  ["/", "Dashboard", LayoutDashboard],
  ["/repositories", "Repositories", FolderGit2],
  ["/chat", "AI Chat", Bot],
  ["/agents", "Agents", BrainCircuit],
  ["/analysis", "Analysis", Code2],
  ["/ml", "ML Prediction", ChartNoAxesColumn],
  ["/documents", "Documentation", FileText],
];

export default function Shell() {
  const { user, logout } = useAuth();
  const { dark, setDark } = useTheme();
  return (
    <div className="ambient min-h-screen bg-slate-50 dark:bg-ink">
      <aside className="fixed inset-y-0 left-0 hidden w-64 border-r border-slate-200 bg-white/80 p-5 backdrop-blur dark:border-white/10 dark:bg-ink/70 lg:block">
        <div className="mb-10 flex items-center gap-3"><div className="rounded-xl bg-accent p-2"><BrainCircuit size={22} className="text-white" /></div><div><p className="font-semibold">DevAgents</p><p className="text-xs text-slate-500">Engineering OS</p></div></div>
        <nav className="space-y-1">{navigation.map(([path, label, Icon]) => <NavLink key={path} to={path} end={path === "/"} className={({ isActive }) => `flex items-center gap-3 rounded-xl px-3 py-3 text-sm transition ${isActive ? "bg-accent/10 text-accent" : "text-slate-500 hover:bg-slate-100 dark:hover:bg-white/5"}`}>{createElement(Icon, { size: 18 })}{label}</NavLink>)}</nav>
      </aside>
      <div className="lg:pl-64">
        <header className="flex h-16 items-center justify-between border-b border-slate-200 bg-white/55 px-5 backdrop-blur dark:border-white/10 dark:bg-ink/40 lg:px-8">
          <p className="text-sm text-slate-500">Multi-Agent AI Software Engineering Assistant</p>
          <div className="flex items-center gap-3">
            <button className="button-secondary !p-2.5" onClick={() => setDark(!dark)}>{dark ? <Sun size={17} /> : <Moon size={17} />}</button>
            <span className="hidden text-sm text-slate-500 sm:inline">{user?.full_name}</span>
            <button className="button-secondary !p-2.5" onClick={logout}><LogOut size={17} /></button>
          </div>
        </header>
        <div className="flex gap-2 overflow-x-auto border-b border-slate-200 p-3 dark:border-white/10 lg:hidden">{navigation.map(([path, label]) => <NavLink className="whitespace-nowrap rounded-lg px-3 py-2 text-xs" key={path} to={path}>{label}</NavLink>)}</div>
        <main className="p-5 lg:p-8"><Outlet /></main>
      </div>
    </div>
  );
}
