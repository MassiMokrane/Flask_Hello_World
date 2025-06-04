# Étape 1 : Image de base
FROM python:3.10-slim

# Étape 2 : Installer les dépendances
RUN pip install flask

# Étape 3 : Définir le répertoire de travail
WORKDIR /app

# Étape 4 : Copier tous les fichiers dans le conteneur
COPY . /app

# Étape 5 : Exposer le port Flask
EXPOSE 5000

# Étape 6 : Lancer le serveur Flask
CMD ["python", "__init__.py"]
