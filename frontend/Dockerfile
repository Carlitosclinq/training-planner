FROM node:18-alpine

WORKDIR /app

# Installation des dépendances
COPY package*.json ./
RUN npm install

# Copie des fichiers source
COPY . .

# Construction de l'application
RUN npm run build

# Installation du serveur HTTP léger
RUN npm install -g serve

# Exposer le port
EXPOSE 3000

# Démarrer l'application
CMD ["serve", "-s", "build", "-l", "3000"]