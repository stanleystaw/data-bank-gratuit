# Dockerfile - Data Bank - Stocke WiFi + Bonus Nuit Celtiis - Sans carte, sans MiFi
FROM python:3.11-slim

WORKDIR /app

# Dépendances système
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie tout le projet
COPY . .

# Crée dossiers data
RUN mkdir -p /app/final_real_bank/cache /app/wifi_server/cache /app/cloud_vps_bank/cache /app/no_card_solution/cache /app/ultimate_bank/cache

# Expose port
EXPOSE 5000

# Variables d'environnement
ENV FLASK_APP=app_no_card.py
ENV PYTHONUNBUFFERED=1

# Commande par défaut - Solution sans carte, sans MiFi, sans laisser PC
CMD ["python", "app_no_card.py"]
