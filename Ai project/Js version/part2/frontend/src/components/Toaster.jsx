import { useToast } from "../state/ToastContext.jsx";
import { Close } from "../lib/icons.jsx";

export default function Toaster() {
  const { toasts, dismiss } = useToast();
  if (toasts.length === 0) return null;

  return (
    <div className="toasts" role="status" aria-live="polite">
      {toasts.map((toast) => (
        <div className="toast" key={toast.id}>
          <span>{toast.message}</span>
          <button type="button" onClick={() => dismiss(toast.id)} aria-label="Fermer">
            <Close width="15" height="15" />
          </button>
        </div>
      ))}
    </div>
  );
}
