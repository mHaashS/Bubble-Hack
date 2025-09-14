# --- Dockerfile Backend Bubble Cleaner Optimisé ---

# Base Python slim
FROM python:3.10-slim

# Définir le répertoire de travail
WORKDIR /app

# Installer dépendances système nécessaires
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    build-essential \
    python3-dev \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    wget \
 && rm -rf /var/lib/apt/lists/*

# Copier uniquement requirements.txt d'abord pour profiter du cache Docker
COPY requirements.txt .

# Installer pip à jour et dépendances IA CPU compatibles
RUN pip install --upgrade pip \
 && pip install --no-cache-dir torch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2 \
 && pip install --no-cache-dir git+https://github.com/facebookresearch/detectron2.git \
 && pip install --no-cache-dir -r requirements.txt \
 && pip install --no-cache-dir huggingface_hub \
 && rm -rf /root/.cache/*

# Créer le dossier pour le modèle (téléchargement au runtime)
RUN mkdir -p /app/models_ai

# Copier uniquement le code source nécessaire
COPY . .

# Exposer le port pour FastAPI
EXPOSE 8000

# Commande par défaut pour lancer Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
