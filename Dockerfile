# Utiliser une image Python légère
FROM python:3.10-slim

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    gcc \
    libc-dev \
    libpq-dev \
    python3-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copier requirements.txt dans le conteneur
COPY requirements.txt /app/requirements.txt

# Mettre à jour pip
RUN pip install --upgrade pip

# Installer les dépendances
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copier tout le projet dans le conteneur
COPY . /app/

# Exposer le port 8000 pour l'API
EXPOSE 8000

# Commande par défaut pour démarrer l'API
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
