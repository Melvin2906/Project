# Backend chat — Flask (src/python/server.py), servi par gunicorn.
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Les dépendances d'abord : cette couche reste en cache tant que
# requirements.docker.txt ne change pas, même si le code bouge.
COPY src/python/requirements.docker.txt ./src/python/
RUN pip install -r src/python/requirements.docker.txt

COPY src/python/ ./src/python/

# server.py ouvre "src/python/temp/history.db" en chemin RELATIF :
# le processus doit donc tourner depuis /app. Le dossier est créé ici
# avec le bon propriétaire pour que le volume monté hérite des droits.
RUN useradd --create-home --uid 10001 app \
 && mkdir -p src/python/temp \
 && chown -R app:app src/python/temp
USER app

EXPOSE 5000

# Un seul worker : la limite de débit (flask-limiter) et le client Gemini
# vivent en mémoire, plusieurs workers ne partageraient rien.
# Des threads pour encaisser plusieurs requêtes en parallèle, et un timeout
# large parce qu'une génération d'image Gemini peut prendre du temps.
CMD ["gunicorn", "--pythonpath", "src/python", "--bind", "0.0.0.0:5000", \
     "--workers", "1", "--threads", "8", "--timeout", "180", \
     "--access-logfile", "-", "server:app"]
