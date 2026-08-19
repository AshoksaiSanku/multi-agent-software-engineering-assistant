import { createContext, useContext, useEffect, useMemo, useState } from "react";
import { api } from "../lib/api";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(Boolean(localStorage.getItem("access_token")));

  useEffect(() => {
    if (!localStorage.getItem("access_token")) return;
    api("/auth/me")
      .then(setUser)
      .catch(() => localStorage.removeItem("access_token"))
      .finally(() => setLoading(false));
  }, []);

  async function authenticate(path, payload) {
    const response = await api(`/auth/${path}`, { method: "POST", body: JSON.stringify(payload) });
    localStorage.setItem("access_token", response.access_token);
    setUser(response.user);
  }

  function logout() {
    localStorage.removeItem("access_token");
    setUser(null);
  }

  const value = useMemo(
    () => ({ user, loading, login: (body) => authenticate("login", body), register: (body) => authenticate("register", body), logout }),
    [user, loading],
  );
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export const useAuth = () => useContext(AuthContext);

