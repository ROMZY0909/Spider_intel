# ✅ Image Python complète + librairies système nécessaires pour WeasyPrint
FROM python:3.11-slim

# ✅ Empêche les prompts interactifs
ENV DEBIAN_FRONTEND=noninteractive

# ✅ Répertoire de travail
WORKDIR /app

# ✅ Installation des dépendances système pour WeasyPrint
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libcairo2 \
    libgdk-pixbuf2.0-0 \
    libxml2 \
    libgobject-2.0-0 \
    libssl-dev \
    shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

# ✅ Copie du projet
COPY . .

# ✅ Installation des dépendances Python
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# ✅ Port
ENV PORT=10000
EXPOSE $PORT

# ✅ Permission d’exécution du script de démarrage (si nécessaire)
RUN chmod +x start.sh

# ✅ Lancement
CMD ["./start.sh"]
