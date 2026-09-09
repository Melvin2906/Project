import { useCallback, useEffect, useRef, useState } from "react";
import { api, ApiError } from "../lib/api.js";
import { useToast } from "./ToastContext.jsx";
import { useAuth } from "./AuthContext.jsx";

let localId = 1;
const uid = () => `m${localId++}`;

const COMMANDS = [
  { prefix: "/image", kind: "image" },
  { prefix: "/pdf", kind: "pdf" },
  { prefix: "/doc", kind: "docx" },
  { prefix: "/excel", kind: "xlsx" },
];

function detectCommand(text) {
  const lower = text.trim().toLowerCase();
  return COMMANDS.find((c) => lower.startsWith(c.prefix)) ?? null;
}

/** Source de vérité de la conversation courante et de l'historique. */
export function useChat() {
  const { logout } = useAuth();
  const { notify } = useToast();

  const [conversations, setConversations] = useState([]);
  const [conversationId, setConversationId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [pending, setPending] = useState(false);
  const [loadingThread, setLoadingThread] = useState(false);
  const abortRef = useRef(null);

  const handle = useCallback(
    (err) => {
      if (err.name === "AbortError") return;
      if (err instanceof ApiError && err.status === 401) {
        notify("Session expirée. Reconnecte-toi.");
        logout();
        return;
      }
      notify(err.message || "Une erreur est survenue.");
    },
    [logout, notify]
  );

  const refresh = useCallback(async () => {
    try {
      const list = await api.listConversations();
      setConversations(Array.isArray(list) ? list : []);
    } catch (err) {
      handle(err);
    }
  }, [handle]);

  useEffect(() => {
    refresh();
  }, [refresh]);

  const openConversation = useCallback(
    async (id) => {
      setConversationId(id);
      setLoadingThread(true);
      try {
        const rows = await api.messages(id);
        setMessages(
          (rows ?? []).map((row) => ({
            id: uid(),
            role: row.role === "user" ? "user" : "assistant",
            content: row.content ?? "",
          }))
        );
      } catch (err) {
        handle(err);
        setMessages([]);
      } finally {
        setLoadingThread(false);
      }
    },
    [handle]
  );

  const newConversation = useCallback(() => {
    abortRef.current?.abort();
    setConversationId(null);
    setMessages([]);
  }, []);

  const removeConversation = useCallback(
    async (id) => {
      const previous = conversations;
      setConversations((list) => list.filter((c) => c.id !== id));
      if (id === conversationId) newConversation();
      try {
        await api.deleteConversation(id);
      } catch (err) {
        setConversations(previous);
        handle(err);
      }
    },
    [conversations, conversationId, handle, newConversation]
  );

  const send = useCallback(
    async (text, files = []) => {
      const trimmed = text.trim();
      if ((!trimmed && files.length === 0) || pending) return;

      const controller = new AbortController();
      abortRef.current = controller;
      setPending(true);

      setMessages((list) => [
        ...list,
        { id: uid(), role: "user", content: trimmed, files: files.map((f) => f.name) },
      ]);

      try {
        let id = conversationId;
        if (!id) {
          const created = await api.createConversation(trimmed.slice(0, 48) || "Nouvelle conversation");
          id = created.id;
          setConversationId(id);
          setConversations((list) => [{ id, title: created.title }, ...list]);
        }

        const command = detectCommand(trimmed);
        let reply;

        if (command && command.kind === "image") {
          const blob = await api.generateImage(
            trimmed.slice(command.prefix.length).trim(),
            controller.signal
          );
          reply = { id: uid(), role: "assistant", kind: "image", url: URL.createObjectURL(blob) };
        } else if (command) {
          const blob = await api.generateDoc(trimmed, command.kind, controller.signal);
          reply = {
            id: uid(),
            role: "assistant",
            kind: "file",
            url: URL.createObjectURL(blob),
            filename: `export.${command.kind}`,
          };
        } else {
          const image = files.find((f) => f.type.startsWith("image/"));
          const doc = files.find((f) => !f.type.startsWith("image/"));
          let data;
          if (image) data = await api.askImage(trimmed, id, image, controller.signal);
          else if (doc) data = await api.askDocument(trimmed, id, doc, controller.signal);
          else data = await api.ask(trimmed, id, controller.signal);
          reply = { id: uid(), role: "assistant", content: data.reply ?? "" };
        }

        setMessages((list) => [...list, reply]);
      } catch (err) {
        handle(err);
        setMessages((list) => [
          ...list,
          {
            id: uid(),
            role: "assistant",
            error: true,
            content: err.message || "La réponse n'est pas arrivée.",
          },
        ]);
      } finally {
        setPending(false);
        abortRef.current = null;
      }
    },
    [conversationId, handle, pending]
  );

  const stop = useCallback(() => abortRef.current?.abort(), []);

  return {
    conversations,
    conversationId,
    messages,
    pending,
    loadingThread,
    send,
    stop,
    openConversation,
    newConversation,
    removeConversation,
    refresh,
  };
}
