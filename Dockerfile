# Étape 1 : image de build
FROM python:3.12-slim AS builder
WORKDIR /app

# Copier et installer les dépendances
COPY requirements.txt .
RUN pip install --prefix=/install -r requirements.txt

# Étape 2 : image finale
FROM python:3.12-slim
WORKDIR /app

# Copier les packages installés
COPY --from=builder /install /usr/local

# Copier le projet
COPY . .

# Exposer le port pour Railway
EXPOSE 8000

# Commande pour démarrer Django
CMD ["gunicorn", "app.wsgi", "--bind", "0.0.0.0:8000"]
