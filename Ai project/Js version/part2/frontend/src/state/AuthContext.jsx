import { createContext, useCallback, useContext, useMemo, useState } from "react";
import { api } from "../lib/api.js";

const AuthContext = createContext(null);

function readSession() {
  const token = localStorage.getItem("token");
  if (!token) return null;
  return {
    token,
    username: localStorage.getItem("username") || "",
    email: localStorage.getItem("email") || "",
  };
}

function writeSession(data) {
  localStorage.setItem("token", data.token);
  localStorage.setItem("username", data.username ?? "");
  localStorage.setItem("email", data.email ?? "");
}

export function AuthProvider({ children }) {
  const [user, setUser] = useState(readSession);

  const login = useCallback(async (email, password) => {
    const data = await api.login(email, password);
    writeSession(data);
    setUser(readSession());
  }, []);

  const register = useCallback(async (username, email, password) => {
    await api.register(username, email, password);
    const data = await api.login(email, password);
    writeSession(data);
    setUser(readSession());
  }, []);

  const logout = useCallback(() => {
    localStorage.removeItem("token");
    localStorage.removeItem("username");
    localStorage.removeItem("email");
    setUser(null);
  }, []);

  const value = useMemo(() => ({ user, login, register, logout }), [user, login, register, logout]);
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth doit être utilisé dans <AuthProvider>");
  return ctx;
}
