# Utiliser Node.js comme image de base
FROM node:18-alpine

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers package*.json
COPY package*.json ./

# Installer les dépendances
RUN npm install

# Copier le reste des fichiers
COPY . .

# Copier le fichier .env
COPY .env ./

# Exposer le port
EXPOSE 5000

# Démarrer l'application
CMD ["npm", "start"]
