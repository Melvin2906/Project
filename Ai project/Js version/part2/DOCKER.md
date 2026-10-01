# Lancer Bouchoura avec Docker

Prérequis : Docker et le plugin Compose (`docker compose version`).

```bash
docker compose up --build -d
```

Puis ouvre http://localhost:8080. Le premier lancement prend quelques
minutes, les suivants quelques secondes.

## Ce qui tourne

| Service | Rôle                          | Accessible depuis ta machine |
|---------|-------------------------------|------------------------------|
| `web`   | nginx : le front + relais API | oui, port 8080               |
| `auth`  | Express, `/register` `/login` | non, via `/api/auth/`        |
| `chat`  | Flask + gunicorn              | non, via `/api/chat/`        |
| `mysql` | comptes utilisateurs          | non (voir docker-compose)    |

Le navigateur ne parle qu'à nginx, qui relaie vers les deux backends.
Tout est sur la même origine : plus besoin de régler `CORS_ORIGIN`.

## Le fichier .env

Le même qu'en local, à la racine. Trois points :

- `DB_USER` doit valoir `root` : le conteneur MySQL crée root avec
  `DB_PASSWORD` comme mot de passe. `DB_PASSWORD` ne peut pas être vide.
- `DB_HOST` est ignoré, Compose le force à `mysql`.
- `OLLAMA_*` est inutile : `server.py` utilise Gemini.

## Données

Deux volumes nommés survivent aux `down` / `up` :

- `mysql-data` : les comptes.
- `chat-data` : `history.db`, les conversations.

Le schéma `database/chatbotdb.sql` n'est joué qu'au **premier**
démarrage. Si tu modifies le schéma, il faut repartir d'un volume vide :

```bash
docker compose down -v    # -v efface AUSSI tes données
```

## Commandes utiles

```bash
docker compose logs -f chat     # suivre les logs d'un service
docker compose ps               # état des services
docker compose restart auth     # relancer un service après un changement de .env
docker compose up --build -d    # reconstruire après un changement de code
docker compose down             # tout arrêter (données conservées)
```
