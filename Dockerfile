FROM python:3.11-slim

WORKDIR /app

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copier et installer les dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code
COPY . .

# Créer le dossier data
RUN mkdir -p /app/data

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]