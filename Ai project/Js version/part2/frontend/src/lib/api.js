import { AUTH_BASE, CHAT_BASE } from "./config.js";

export class ApiError extends Error {
  constructor(message, status) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

const MESSAGES = {
  401: "Session expirée. Reconnecte-toi pour continuer.",
  403: "Cette conversation ne t'appartient pas.",
  404: "Introuvable.",
  429: "Trop de messages d'affilée. Attends quelques secondes.",
  500: "Le serveur a échoué à répondre.",
};

function token() {
  return localStorage.getItem("token");
}

async function request(base, path, { method = "GET", body, json = true, signal } = {}) {
  const headers = {};
  const jwt = token();
  if (jwt) headers.Authorization = `Bearer ${jwt}`;

  let payload = body;
  if (json && body !== undefined && !(body instanceof FormData)) {
    headers["Content-Type"] = "application/json";
    payload = JSON.stringify(body);
  }

  let res;
  try {
    res = await fetch(`${base}${path}`, { method, headers, body: payload, signal });
  } catch (err) {
    if (err.name === "AbortError") throw err;
    throw new ApiError("Serveur injoignable. Vérifie qu'il tourne bien.", 0);
  }

  if (!res.ok) {
    const data = await res.json().catch(() => ({}));
    throw new ApiError(data.error || MESSAGES[res.status] || `Erreur ${res.status}`, res.status);
  }

  return res;
}

async function asJson(...args) {
  const res = await request(...args);
  return res.status === 204 ? null : res.json();
}

export const api = {
  register: (username, email, password) =>
    asJson(AUTH_BASE, "/register", { method: "POST", body: { username, email, password } }),

  login: (email, password) =>
    asJson(AUTH_BASE, "/login", { method: "POST", body: { email, password } }),

  listConversations: () => asJson(CHAT_BASE, "/conversations"),

  createConversation: (title = "Nouvelle conversation") =>
    asJson(CHAT_BASE, "/conversations", { method: "POST", body: { title } }),

  deleteConversation: (id) =>
    asJson(CHAT_BASE, `/conversations/${id}`, { method: "DELETE" }),

  messages: (id) => asJson(CHAT_BASE, `/conversations/${id}/messages`),

  ask: (message, conversationId, signal) =>
    asJson(CHAT_BASE, "/ask", {
      method: "POST",
      body: { message, conversation_id: conversationId },
      signal,
    }),

  askImage: (message, conversationId, file, signal) => {
    const form = new FormData();
    form.append("message", message);
    form.append("conversation_id", conversationId);
    form.append("image", file);
    return asJson(CHAT_BASE, "/ask-image", { method: "POST", body: form, signal });
  },

  askDocument: (message, conversationId, file, signal) => {
    const form = new FormData();
    form.append("message", message);
    form.append("conversation_id", conversationId);
    form.append("file", file);
    return asJson(CHAT_BASE, "/ask-document", { method: "POST", body: form, signal });
  },

  generateImage: async (prompt, signal) => {
    const res = await request(CHAT_BASE, "/generate-image", {
      method: "POST",
      body: { prompt },
      signal,
    });
    return res.blob();
  },

  generateDoc: async (prompt, type, signal) => {
    const res = await request(CHAT_BASE, "/generate-doc", {
      method: "POST",
      body: { prompt, type },
      signal,
    });
    return res.blob();
  },

  updateTimezone: (timezone) =>
    asJson(CHAT_BASE, "/update-timezone", { method: "POST", body: { timezone } }),
};
