# 🐍 Image officielle Python 3.11
FROM python:3.11-slim

# 📁 Répertoire de travail dans le conteneur
WORKDIR /app

# 🧪 Copie tous les fichiers du projet dans le conteneur
COPY . .

# 📦 Mise à jour de pip et installation des dépendances
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# ✅ Rend start.sh exécutable
RUN chmod +x start.sh

# 🌐 Port d’écoute pour Render (utilise PORT injecté)
ENV PORT=10000
EXPOSE $PORT

# 🚀 Commande de démarrage
CMD ["./start.sh"]
