import { useEffect, useState } from "react";
import { api } from "../lib/api.js";
import { useToast } from "../state/ToastContext.jsx";
import { Close } from "../lib/icons.jsx";

const TABS = [
  { id: "general", label: "Général" },
  { id: "account", label: "Compte" },
  { id: "data", label: "Données" },
];

export default function SettingsDialog({ user, theme, setTheme, voiceLang, setVoiceLang, onClose }) {
  const [tab, setTab] = useState("general");
  const { notify } = useToast();

  useEffect(() => {
    const onKey = (event) => event.key === "Escape" && onClose();
    document.addEventListener("keydown", onKey);
    return () => document.removeEventListener("keydown", onKey);
  }, [onClose]);

  const syncTimezone = async () => {
    const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
    try {
      await api.updateTimezone(timezone);
      notify(`Fuseau réglé sur ${timezone}.`);
    } catch (error) {
      notify(error.message);
    }
  };

  return (
    <div className="scrim" onMouseDown={(e) => e.target === e.currentTarget && onClose()}>
      <div className="dialog" role="dialog" aria-modal="true" aria-label="Réglages">
        <div className="dialog__nav" role="tablist">
          {TABS.map((item) => (
            <button
              key={item.id}
              type="button"
              role="tab"
              aria-selected={tab === item.id}
              onClick={() => setTab(item.id)}
            >
              {item.label}
            </button>
          ))}
        </div>

        <div className="dialog__panel" role="tabpanel">
          <div className="dialog__head">
            <h2 className="dialog__title">{TABS.find((t) => t.id === tab)?.label}</h2>
            <button type="button" className="icon-button" onClick={onClose} aria-label="Fermer les réglages">
              <Close />
            </button>
          </div>

          {tab === "general" && (
            <>
              <div className="row">
                <div>
                  <strong>Apparence</strong>
                  <p>Suit ton système par défaut.</p>
                </div>
                <select className="select" value={theme} onChange={(e) => setTheme(e.target.value)}>
                  <option value="system">Système</option>
                  <option value="light">Clair</option>
                  <option value="dark">Sombre</option>
                </select>
              </div>

              <div className="row">
                <div>
                  <strong>Langue de la dictée</strong>
                  <p>Utilisée pour le micro et la lecture à voix haute.</p>
                </div>
                <select className="select" value={voiceLang} onChange={(e) => setVoiceLang(e.target.value)}>
                  <option value="fr-FR">Français</option>
                  <option value="en-US">Anglais</option>
                </select>
              </div>

              <div className="row">
                <div>
                  <strong>Fuseau horaire</strong>
                  <p>Permet au modèle de donner l'heure correcte.</p>
                </div>
                <button type="button" className="button button--ghost" onClick={syncTimezone}>
                  Synchroniser
                </button>
              </div>
            </>
          )}

          {tab === "account" && (
            <>
              <div className="row">
                <div>
                  <strong>Nom</strong>
                  <p>{user?.username || "—"}</p>
                </div>
              </div>
              <div className="row">
                <div>
                  <strong>Email</strong>
                  <p>{user?.email || "—"}</p>
                </div>
              </div>
            </>
          )}

          {tab === "data" && (
            <div className="row">
              <div>
                <strong>Historique</strong>
                <p>Supprime une conversation depuis la liste de gauche pour l'effacer du serveur.</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
