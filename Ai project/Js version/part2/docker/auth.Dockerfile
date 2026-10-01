# Backend auth — Express (src/server.js) : /register, /login.
FROM node:22-slim

ENV NODE_ENV=production
WORKDIR /app

# npm ci reconstruit node_modules À L'INTÉRIEUR du conteneur. Indispensable :
# bcrypt est un module natif, celui compilé sur ta machine ne tourne pas ici.
COPY package.json package-lock.json ./
RUN npm ci --omit=dev

COPY src/server.js ./src/server.js

USER node
EXPOSE 3000
CMD ["node", "src/server.js"]
