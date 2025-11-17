# Dockerfile
FROM python:3.11-slim

# Variables d'environnement pour Dash
ENV PYTHONUNBUFFERED=1
ENV DASH_DEBUG=True

# Créer un dossier pour l'app
WORKDIR /app

# Copier les fichiers de l'application
COPY app.py /app/
COPY data /app/data

# Installer les dépendances
RUN pip install --no-cache-dir dash pandas plotly

# Exposer le port Dash
EXPOSE 8050

# Lancer l'application
CMD ["python", "app.py"]
