# Utiliser une image Python officielle légère
FROM python:3.12-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier requirements.txt depuis le contexte de build (la racine du repo)
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source de l'application
COPY meteo/ ./meteo/

# Définir la commande par défaut pour lancer l'application
CMD ["python", "-m", "meteo"]
