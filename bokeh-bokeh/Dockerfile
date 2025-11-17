FROM python:3.11-slim

# Pour éviter les questions pendant apt-get
ENV DEBIAN_FRONTEND=noninteractive

# Installation des dépendances système minimales (facultatif mais recommandé)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Création du dossier de travail
WORKDIR /app

# Copie des fichiers de config Python
COPY requirements.txt .

# Installation des dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code et des données
COPY app.py .
COPY data ./data

# Expose le port Bokeh par défaut
EXPOSE 5006

# Commande de lancement du serveur Bokeh
# --allow-websocket-origin="*" est pratique en dev ; en prod, mets ton domaine.
CMD ["bokeh", "serve", "app.py", "--port", "5006", "--allow-websocket-origin=*"]
