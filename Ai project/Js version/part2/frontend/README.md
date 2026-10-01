# Bouchoura — frontend v2

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
  styles/    tokens.css (couleurs, type, espacements), app.css, auth.css
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
- Responsive complet : tiroir sous 860 px avec fond cliquable, mise en
  page téléphone sous 560 px, mode paysage, zones sûres (encoche, barre
  de geste), cibles tactiles de 42 px, actions visibles sans survol.
- Installable comme application (manifeste PWA + icône).
- Thème clair/sombre, `:focus-visible` partout,
  `prefers-reduced-motion` respecté.
- Écran de connexion : le panneau coulissant de la v1 est conservé, mais
  scopé sous `.auth-shell` (la v1 stylait `form`, `input`, `button` nus) et
  repliable en un seul formulaire sous 760 px.
- Icônes SVG inline à la place des 18 PNG.
- Markdown assaini par DOMPurify, liens externes en `rel="noopener"`.

## Restant côté backend

- Le titre de conversation est fixé à la création (48 premiers caractères).
  Ajouter `PATCH /conversations/:id` permettrait de le renommer.
- L'auth (Express `:3000`) et le chat (Flask `:5000`) partagent `JWT_SECRET`
  mais sont deux services : à terme, en fusionner un dans l'autre.
- Le streaming n'existe pas encore côté serveur. Dès que `/ask` renvoie du
  SSE, `useChat.send` peut consommer le flux sans changer les composants.

## Changer les couleurs

Tout part de `src/styles/tokens.css`. Les deux thèmes y sont déclarés en
variables : modifie `--bg`, `--surface`, `--text` pour la base, `--amber`
pour l'accent. Aucun composant ne contient de couleur en dur.

## Tester sur ton téléphone

```bash
npm run dev:mobile
```

Vite affiche une adresse du type `http://192.168.1.42:5173` : ouvre-la
sur ton téléphone, connecté au même Wi-Fi.

Attention, sur le téléphone `localhost` désigne **le téléphone**, pas ton
PC. Dans `.env`, remplace donc les deux URL par l'IP du PC :

```
VITE_AUTH_BASE=http://192.168.1.42:3000
VITE_CHAT_BASE=http://192.168.1.42:5000
```

et ajoute `http://192.168.1.42:5173` à `CORS_ORIGIN` côté Express.
Flask doit aussi écouter sur toutes les interfaces (`host="0.0.0.0"`).

## Vers une application mobile

Le front est prêt pour être empaqueté avec Capacitor, qui embarque
cette même application Vite dans une coquille iOS/Android, sans réécriture.
La seule vraie contrainte côté backend : il faudra qu'il soit déployé sur
une URL publique en HTTPS, une app mobile ne peut pas joindre `localhost`.
