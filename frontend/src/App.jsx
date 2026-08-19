import { Navigate, Route, Routes } from "react-router-dom";
import Shell from "./components/Shell";
import { Loader } from "./components/Ui";
import { useAuth } from "./contexts/AuthContext";
import AgentsPage from "./pages/AgentsPage";
import AnalysisPage from "./pages/AnalysisPage";
import ChatPage from "./pages/ChatPage";
import DashboardPage from "./pages/DashboardPage";
import DocumentsPage from "./pages/DocumentsPage";
import LoginPage from "./pages/LoginPage";
import MLPage from "./pages/MLPage";
import RepositoriesPage from "./pages/RepositoriesPage";

function Protected() {
  const { user, loading } = useAuth();
  if (loading) return <div className="flex min-h-screen items-center justify-center"><Loader label="Loading workspace" /></div>;
  return user ? <Shell /> : <Navigate to="/login" replace />;
}

export default function App() {
  const { user } = useAuth();
  return (
    <Routes>
      <Route path="/login" element={user ? <Navigate to="/" replace /> : <LoginPage />} />
      <Route element={<Protected />}>
        <Route index element={<DashboardPage />} />
        <Route path="/repositories" element={<RepositoriesPage />} />
        <Route path="/chat" element={<ChatPage />} />
        <Route path="/agents" element={<AgentsPage />} />
        <Route path="/analysis" element={<AnalysisPage />} />
        <Route path="/ml" element={<MLPage />} />
        <Route path="/documents" element={<DocumentsPage />} />
      </Route>
    </Routes>
  );
}

