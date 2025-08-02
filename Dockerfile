FROM python:3.10-slim-bullseye

# Installer les dépendances système
RUN apt-get update && \
    apt-get install -y build-essential libssl-dev libffi-dev wget && \
    rm -rf /var/lib/apt/lists/*

# Installer TA-Lib
RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && \
    tar -xzf ta-lib-0.4.0-src.tar.gz && \
    cd ta-lib/ && \
    ./configure --prefix=/usr && \
    make && \
    make install && \
    cd .. && \
    rm -rf ta-lib*

# Configurer l'environnement
WORKDIR /app
ENV PYTHONUNBUFFERED=1

# Copier et installer les dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier l'application
COPY . .

# Utiliser un script d'entrée pour résoudre le problème de PORT
CMD ["sh", "-c", "gunicorn app:app --bind 0.0.0.0:${PORT} --timeout 120 --workers 2"]
