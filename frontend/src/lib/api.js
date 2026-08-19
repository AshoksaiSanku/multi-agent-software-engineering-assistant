const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api/v1";
const configuredWebSocketUrl = import.meta.env.VITE_WS_URL || "ws://localhost:8000/api/v1";
export const WS_URL = configuredWebSocketUrl.startsWith("/")
  ? `${window.location.protocol === "https:" ? "wss:" : "ws:"}//${window.location.host}${configuredWebSocketUrl}`
  : configuredWebSocketUrl;

export function token() {
  return localStorage.getItem("access_token");
}

export async function api(path, options = {}) {
  const headers = { "Content-Type": "application/json", ...(options.headers || {}) };
  if (token()) headers.Authorization = `Bearer ${token()}`;
  const response = await fetch(`${API_URL}${path}`, { ...options, headers });
  if (!response.ok) {
    const body = await response.json().catch(() => ({ detail: "Request failed" }));
    throw new Error(body.detail || "Request failed");
  }
  return response.status === 204 ? null : response.json();
}

export async function download(path, filename) {
  const response = await fetch(`${API_URL}${path}`, {
    headers: { Authorization: `Bearer ${token()}` },
  });
  if (!response.ok) throw new Error("Download failed");
  const link = document.createElement("a");
  link.href = URL.createObjectURL(await response.blob());
  link.download = filename;
  link.click();
  URL.revokeObjectURL(link.href);
}
