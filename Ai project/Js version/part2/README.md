# My.AI — frontend v2

Refonte du frontend : une seule application React (Vite) qui remplace
`index.html` + `full-screen.html` + `login_signup.html` et leurs trois scripts.

## Démarrer

```bash
cp .env.example .env   # ajuste les deux URLs si besoin
npm install
npm run dev            # http://localhost:5173
```

Les deux backends doivent tourner en parallèle :
Express (auth) sur `:3000`, Flask (chat) sur `:5000`.
Vérifie que `CORS_ORIGIN` côté serveurs autorise bien `http://localhost:5173`.

## Structure

```
src/
  lib/       api.js (couche réseau unique), markdown.js, icons.jsx, config.js
  state/     AuthContext, ToastContext, useChat (état de la conversation)
  hooks/     useAutoScroll, useSpeech, useTheme
  components/Sidebar, Composer, Message, SettingsDialog, Toaster
  pages/     Auth, Chat
  styles/    tokens.css (couleurs, type, espacements), app.css
```

Une seule règle : les composants ne parlent jamais à `fetch` directement,
tout passe par `lib/api.js`, qui traduit les statuts HTTP en messages lisibles.

## Ce qui est corrigé par rapport à v1

- Historique des conversations réellement affiché, ouvrable et supprimable.
- Défilement automatique tant que tu n'as pas remonté le fil toi-même.
- Erreurs visibles (notification + message dans le fil) au lieu de `console.error`.
- Envoi bloqué pendant une réponse, avec bouton d'annulation (`AbortController`).
- Responsive fonctionnel : la barre latérale devient un tiroir sous 860 px.
  L'ancienne media query était écrasée par la spécificité du nesting CSS.
- Thème clair/sombre, `:focus-visible` partout, `prefers-reduced-motion` respecté.
- Icônes SVG inline à la place des 18 PNG.
- Markdown assaini par DOMPurify, liens externes en `rel="noopener"`.

## Restant côté backend

- Le titre de conversation est fixé à la création (48 premiers caractères).
  Ajouter `PATCH /conversations/:id` permettrait de le renommer.
- L'auth (Express `:3000`) et le chat (Flask `:5000`) partagent `JWT_SECRET`
  mais sont deux services : à terme, en fusionner un dans l'autre.
- Le streaming n'existe pas encore côté serveur. Dès que `/ask` renvoie du
  SSE, `useChat.send` peut consommer le flux sans changer les composants.
