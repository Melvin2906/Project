import { useState } from "react";
import { useAuth } from "../state/AuthContext.jsx";

const SOCIALS = [
  {
    name: "Facebook",
    path: "M14 8.5h2V6h-2c-1.7 0-3 1.3-3 3v1.5H9V13h2v5h2.5v-5H16l.5-2.5h-3V9c0-.3.2-.5.5-.5z",
  },
  {
    name: "Google",
    path: "M18 12.2c0-.5 0-1-.1-1.4H12v2.7h3.4c-.1.8-.6 1.5-1.3 2v1.7h2.1c1.2-1.1 1.8-2.8 1.8-5zM12 19c1.7 0 3.2-.6 4.2-1.6l-2.1-1.6c-.6.4-1.3.6-2.1.6-1.7 0-3.1-1.1-3.6-2.6H6.2v1.7C7.3 17.6 9.5 19 12 19zM8.4 13.8a4.2 4.2 0 010-2.6V9.5H6.2a7 7 0 000 6.3l2.2-2zM12 8c.9 0 1.8.3 2.4 1l1.8-1.8A6.7 6.7 0 0012 5.4c-2.5 0-4.7 1.4-5.8 3.5l2.2 1.7C8.9 9.1 10.3 8 12 8z",
  },
  {
    name: "LinkedIn",
    path: "M7.5 9.5H9.7V18H7.5zM8.6 6a1.3 1.3 0 110 2.6 1.3 1.3 0 010-2.6zM11.4 9.5h2.1v1.2c.4-.7 1.3-1.4 2.5-1.4 2 0 2.6 1.2 2.6 3.2V18h-2.2v-4.9c0-1-.3-1.7-1.3-1.7s-1.5.7-1.5 1.7V18h-2.2z",
  },
];

function Socials() {
  return (
    <div className="socials">
      {SOCIALS.map((social) => (
        <a key={social.name} href="#" aria-label={`Continuer avec ${social.name}`} onClick={(e) => e.preventDefault()}>
          <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
            <path d={social.path} />
          </svg>
        </a>
      ))}
    </div>
  );
}

export default function Auth() {
  const { login, register } = useAuth();
  const [panel, setPanel] = useState("signin");
  const [signin, setSignin] = useState({ email: "", password: "" });
  const [signup, setSignup] = useState({ username: "", email: "", password: "" });
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  const switchTo = (next) => {
    setPanel(next);
    setError("");
  };

  const run = async (action) => {
    setError("");
    setBusy(true);
    try {
      await action();
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  };

  const submitSignin = (event) => {
    event.preventDefault();
    run(() => login(signin.email.trim(), signin.password));
  };

  const submitSignup = (event) => {
    event.preventDefault();
    run(() => register(signup.username.trim(), signup.email.trim(), signup.password));
  };

  return (
    <div className="auth-shell">
      <div className="auth-card" data-panel={panel}>
        {/* Connexion */}
        <div className="auth-panel auth-panel--signin">
          <form className="auth-form" onSubmit={submitSignin}>
            <h2>Se connecter</h2>
            <Socials />
            <p className="auth-form__note">ou avec ton email</p>

            {panel === "signin" && error && <p className="form-error">{error}</p>}

            <div className="field">
              <label htmlFor="signin-email">Email</label>
              <input
                id="signin-email"
                type="email"
                autoComplete="email"
                required
                value={signin.email}
                onChange={(e) => setSignin({ ...signin, email: e.target.value })}
              />
            </div>

            <div className="field">
              <label htmlFor="signin-password">Mot de passe</label>
              <input
                id="signin-password"
                type="password"
                autoComplete="current-password"
                required
                value={signin.password}
                onChange={(e) => setSignin({ ...signin, password: e.target.value })}
              />
            </div>

            <button className="button" type="submit" disabled={busy}>
              {busy ? "Un instant…" : "Se connecter"}
            </button>

            <p className="auth-switch">
              Pas encore de compte ?{" "}
              <button type="button" onClick={() => switchTo("signup")}>En créer un</button>
            </p>
          </form>
        </div>

        {/* Inscription */}
        <div className="auth-panel auth-panel--signup">
          <form className="auth-form" onSubmit={submitSignup}>
            <h2>Créer un compte</h2>
            <Socials />
            <p className="auth-form__note">ou avec ton email</p>

            {panel === "signup" && error && <p className="form-error">{error}</p>}

            <div className="field">
              <label htmlFor="signup-name">Nom</label>
              <input
                id="signup-name"
                autoComplete="name"
                required
                value={signup.username}
                onChange={(e) => setSignup({ ...signup, username: e.target.value })}
              />
            </div>

            <div className="field">
              <label htmlFor="signup-email">Email</label>
              <input
                id="signup-email"
                type="email"
                autoComplete="email"
                required
                value={signup.email}
                onChange={(e) => setSignup({ ...signup, email: e.target.value })}
              />
            </div>

            <div className="field">
              <label htmlFor="signup-password">Mot de passe</label>
              <input
                id="signup-password"
                type="password"
                autoComplete="new-password"
                required
                minLength={8}
                value={signup.password}
                onChange={(e) => setSignup({ ...signup, password: e.target.value })}
              />
            </div>

            <button className="button" type="submit" disabled={busy}>
              {busy ? "Un instant…" : "Créer le compte"}
            </button>

            <p className="auth-switch">
              Déjà inscrit ?{" "}
              <button type="button" onClick={() => switchTo("signin")}>Se connecter</button>
            </p>
          </form>
        </div>

        {/* Volet coulissant */}
        <div className="auth-overlay-frame">
          <div className="auth-overlay">
            <div className="auth-overlay__side auth-overlay__side--left">
              <h3>Content de te revoir</h3>
              <p>Reprends tes conversations là où tu les as laissées.</p>
              <button type="button" className="button--outline" onClick={() => switchTo("signin")}>
                Se connecter
              </button>
            </div>
            <div className="auth-overlay__side auth-overlay__side--right">
              <h3>Première visite ?</h3>
              <p>Crée un compte pour garder ton historique d'une session à l'autre.</p>
              <button type="button" className="button--outline" onClick={() => switchTo("signup")}>
                Créer un compte
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
