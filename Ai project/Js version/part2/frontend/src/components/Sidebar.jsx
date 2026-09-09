import { useEffect, useRef, useState } from "react";
import { Panel, Plus, Trash } from "../lib/icons.jsx";

function initials(name = "") {
  return name.trim().slice(0, 2).toUpperCase() || "?";
}

export default function Sidebar({
  conversations,
  conversationId,
  user,
  onNew,
  onOpen,
  onDelete,
  onToggleRail,
  onOpenSettings,
  onLogout,
}) {
  const [menuOpen, setMenuOpen] = useState(false);
  const footRef = useRef(null);

  useEffect(() => {
    if (!menuOpen) return;
    const onClick = (event) => {
      if (!footRef.current?.contains(event.target)) setMenuOpen(false);
    };
    const onKey = (event) => event.key === "Escape" && setMenuOpen(false);
    document.addEventListener("mousedown", onClick);
    document.addEventListener("keydown", onKey);
    return () => {
      document.removeEventListener("mousedown", onClick);
      document.removeEventListener("keydown", onKey);
    };
  }, [menuOpen]);

  return (
    <aside className="sidebar">
      <div className="sidebar__head">
        <h1 className="wordmark">
          My<span>.</span>AI
        </h1>
        <button type="button" className="icon-button" onClick={onToggleRail} aria-label="Replier le panneau">
          <Panel />
        </button>
      </div>

      <button type="button" className="sidebar__new" onClick={onNew}>
        <Plus />
        <span>Nouvelle conversation</span>
      </button>

      <nav className="history" aria-label="Conversations">
        {conversations.length === 0 ? (
          <p className="history__empty">Tes conversations s'afficheront ici.</p>
        ) : (
          conversations.map((conversation) => (
            <div
              key={conversation.id}
              className="history__item"
              aria-current={conversation.id === conversationId}
            >
              <button
                type="button"
                className="history__title"
                onClick={() => onOpen(conversation.id)}
              >
                {conversation.title || "Sans titre"}
              </button>
              <button
                type="button"
                className="history__delete"
                onClick={() => onDelete(conversation.id)}
                aria-label={`Supprimer ${conversation.title || "cette conversation"}`}
              >
                <Trash />
              </button>
            </div>
          ))
        )}
      </nav>

      <div className="sidebar__foot" ref={footRef} style={{ position: "relative" }}>
        <button
          type="button"
          className="account"
          onClick={() => setMenuOpen((open) => !open)}
          aria-haspopup="menu"
          aria-expanded={menuOpen}
        >
          <span className="avatar" aria-hidden="true">{initials(user?.username || user?.email)}</span>
          <span className="account__name">{user?.username || user?.email || "Invité"}</span>
        </button>

        {menuOpen && (
          <div className="menu" role="menu">
            <button type="button" role="menuitem" onClick={() => { setMenuOpen(false); onOpenSettings(); }}>
              Réglages
            </button>
            <button type="button" role="menuitem" onClick={onLogout}>
              Se déconnecter
            </button>
          </div>
        )}
      </div>
    </aside>
  );
}
