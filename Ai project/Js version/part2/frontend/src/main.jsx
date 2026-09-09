import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import App from "./App.jsx";
import { AuthProvider } from "./state/AuthContext.jsx";
import { ToastProvider } from "./state/ToastContext.jsx";
import "./styles/tokens.css";
import "./styles/app.css";
import "./styles/auth.css";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <ToastProvider>
      <AuthProvider>
        <App />
      </AuthProvider>
    </ToastProvider>
  </StrictMode>
);
