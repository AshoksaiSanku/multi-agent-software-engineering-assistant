import { createContext, useContext, useState } from "react";
import { X } from "lucide-react";

const ToastContext = createContext(null);

export function ToastProvider({ children }) {
  const [toasts, setToasts] = useState([]);
  function notify(message, kind = "success") {
    const id = Date.now();
    setToasts((items) => [...items, { id, message, kind }]);
    setTimeout(() => setToasts((items) => items.filter((item) => item.id !== id)), 3500);
  }
  return (
    <ToastContext.Provider value={notify}>
      {children}
      <div className="fixed right-5 top-5 z-50 space-y-3">
        {toasts.map((toast) => (
          <div key={toast.id} className={`flex min-w-72 items-center justify-between rounded-xl border p-4 text-sm shadow-xl ${toast.kind === "error" ? "border-red-500/30 bg-red-950 text-red-100" : "border-aqua/20 bg-panel text-slate-100"}`}>
            {toast.message}
            <button onClick={() => setToasts((items) => items.filter((item) => item.id !== toast.id))}><X size={16} /></button>
          </div>
        ))}
      </div>
    </ToastContext.Provider>
  );
}

export const useToast = () => useContext(ToastContext);

