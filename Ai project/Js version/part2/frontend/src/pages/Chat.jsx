import { useEffect, useState } from "react";
import Sidebar from "../components/Sidebar.jsx";
import Composer from "../components/Composer.jsx";
import Message from "../components/Message.jsx";
import SettingsDialog from "../components/SettingsDialog.jsx";
import { useChat } from "../state/useChat.js";
import { useAuth } from "../state/AuthContext.jsx";
import { useAutoScroll } from "../hooks/useAutoScroll.js";
import { useSpeech } from "../hooks/useSpeech.js";
import { useTheme } from "../hooks/useTheme.js";
import { Panel, Plus } from "../lib/icons.jsx";

const STARTERS = [
  { title: "Explique-moi un concept", hint: "« Explique les WebSockets avec une analogie »" },
  { title: "Analyse un document", hint: "Joins un PDF et pose ta question dessus" },
  { title: "Génère une image", hint: "/image un renard dans une forêt de pins" },
  { title: "Produis un fichier", hint: "/pdf un compte-rendu de réunion" },
];

export default function Chat() {
  const { user, logout } = useAuth();
  const chat = useChat();
  const [rail, setRail] = useState(false);
  const [drawer, setDrawer] = useState(false);
  const [settings, setSettings] = useState(false);
  const [theme, setTheme] = useTheme();
  const [voiceLang, setVoiceLang] = useState(() => localStorage.getItem("voiceLang") || "fr-FR");

  const speech = useSpeech({
    lang: voiceLang,
    onResult: (text) => chat.send(text),
  });

  const { ref: threadRef } = useAutoScroll([chat.messages, chat.pending]);

  // Tiroir mobile : Échap le ferme, et la page derrière ne défile plus.
  useEffect(() => {
    if (!drawer) return;
    const onKey = (event) => event.key === "Escape" && setDrawer(false);
    document.addEventListener("keydown", onKey);
    document.body.style.overflow = "hidden";
    return () => {
      document.removeEventListener("keydown", onKey);
      document.body.style.overflow = "";
    };
  }, [drawer]);

  // Repasser en grand écran avec le tiroir ouvert ne doit rien bloquer.
  useEffect(() => {
    const query = window.matchMedia("(min-width: 861px)");
    const onChange = (event) => event.matches && setDrawer(false);
    query.addEventListener("change", onChange);
    return () => query.removeEventListener("change", onChange);
  }, []);

  const changeVoiceLang = (value) => {
    setVoiceLang(value);
    localStorage.setItem("voiceLang", value);
  };

  const openConversation = (id) => {
    chat.openConversation(id);
    setDrawer(false);
  };

  return (
    <div className="app" data-rail={rail} data-drawer={drawer}>
      <Sidebar
        conversations={chat.conversations}
        conversationId={chat.conversationId}
        user={user}
        onNew={() => {
          chat.newConversation();
          setDrawer(false);
        }}
        onOpen={openConversation}
        onDelete={chat.removeConversation}
        onToggleRail={() => (window.innerWidth <= 860 ? setDrawer(false) : setRail((v) => !v))}
        onOpenSettings={() => {
          setDrawer(false);
          setSettings(true);
        }}
        onLogout={logout}
      />

      <div className="drawer-scrim" onClick={() => setDrawer(false)} aria-hidden="true" />

      <main className="main">
        <div className="topbar">
          <button
            type="button"
            className="icon-button"
            onClick={() => setDrawer((v) => !v)}
            aria-label="Ouvrir les conversations"
            aria-expanded={drawer}
          >
            <Panel />
          </button>
          <strong style={{ flex: 1 }}>Bouchoura</strong>
          <button
            type="button"
            className="icon-button"
            onClick={chat.newConversation}
            aria-label="Nouvelle conversation"
          >
            <Plus />
          </button>
        </div>

        <div className="thread" ref={threadRef}>
          <div className="thread__inner">
            {chat.messages.length === 0 && !chat.loadingThread ? (
              <section className="empty">
                <h2 className="empty__title">
                  Bonjour {user?.username?.split(" ")[0] || ""}, on commence par quoi&nbsp;?
                </h2>
                <p className="empty__sub">
                  Pose une question, joins un fichier, ou lance une commande.
                </p>
                <div className="prompts">
                  {STARTERS.map((starter) => (
                    <button
                      key={starter.title}
                      type="button"
                      className="prompt"
                      onClick={() => chat.send(starter.hint.replace(/[«»]/g, "").trim())}
                    >
                      <strong>{starter.title}</strong>
                      <span>{starter.hint}</span>
                    </button>
                  ))}
                </div>
              </section>
            ) : (
              chat.messages.map((message) => (
                <Message key={message.id} message={message} onSpeak={(text) => speech.speak(text, voiceLang)} />
              ))
            )}

            {chat.pending && (
              <div className="msg msg--assistant">
                <span className="thinking" aria-label="Réponse en cours">
                  <i /><i /><i />
                </span>
              </div>
            )}
          </div>
        </div>

        <Composer pending={chat.pending} onSend={chat.send} onStop={chat.stop} speech={speech} />
      </main>

      {settings && (
        <SettingsDialog
          user={user}
          theme={theme}
          setTheme={setTheme}
          voiceLang={voiceLang}
          setVoiceLang={changeVoiceLang}
          onClose={() => setSettings(false)}
        />
      )}
    </div>
  );
}
