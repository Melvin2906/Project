# Frontend — build Vite, puis servi statiquement par nginx.

# ── Étape 1 : construction ───────────────────────────────
FROM node:22-alpine AS build
WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY . .

# Les variables VITE_* sont figées dans le JavaScript AU MOMENT DU BUILD.
# Des chemins relatifs : le front appelle sa propre origine, nginx relaie.
ARG VITE_AUTH_BASE=/api/auth
ARG VITE_CHAT_BASE=/api/chat
ENV VITE_AUTH_BASE=$VITE_AUTH_BASE \
    VITE_CHAT_BASE=$VITE_CHAT_BASE

RUN npm run build

# ── Étape 2 : service ────────────────────────────────────
FROM nginx:1.27-alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
