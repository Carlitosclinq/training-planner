FROM python:3.11-slim

WORKDIR /app

# Installation des dépendances système
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Installation des dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie des fichiers source
COPY . .

# Exposer le port
EXPOSE 8000

# Démarrer l'application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]