# ✅ Base Python 3.11
FROM python:3.11-slim

# ✅ Prévenir les prompts
ENV DEBIAN_FRONTEND=noninteractive

# ✅ Répertoire de travail
WORKDIR /app

# ✅ Dépendances système pour WeasyPrint
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libglib2.0-0 \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libxml2 \
    libssl-dev \
    shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

# ✅ Copie du projet
COPY . .

# ✅ Installer pip + dépendances Python
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# ✅ Port d'écoute Render
ENV PORT=10000
EXPOSE $PORT

# ✅ Démarrage
RUN chmod +x start.sh
CMD ["./start.sh"]
