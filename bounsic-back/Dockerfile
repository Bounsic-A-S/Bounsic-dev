# Etapa 1: Builder
FROM python:3.11-slim AS builder

WORKDIR /app

# Evita la escritura de archivos .pyc y usa buffer de logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Instala dependencias del sistema necesarias
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libffi-dev \
    libsndfile1 \
    ffmpeg \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libpq-dev \
    curl \
    unzip \
    chromium-driver \
    chromium \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Instala dependencias Python
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --prefix=/install -r requirements.txt
    pip install --prefix=/install gunicorn

# Etapa 2: Imagen final
FROM python:3.11-slim

WORKDIR /app

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/install/bin:$PATH" \
    GOOGLE_CHROME_BIN=/usr/bin/chromium \
    CHROMEDRIVER_PATH=/usr/bin/chromedriver

# Instala runtime necesario
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    chromium-driver \
    chromium \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copia dependencias instaladas
COPY --from=builder /install /usr/local

# Copia el código fuente
COPY . .
COPY cookies/ ./cookies/

# Copia los certificados SSL
COPY cert/privkey.pem /app/cert/key.pem
COPY cert/fullchain.pem /app/cert/cert.pem

# Puerto expuesto
EXPOSE 443

# Comando de inicio del servidor FastAPI en HTTPS con Gunicorn y Uvicorn Workers
CMD ["gunicorn", "app.main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:443", "--keyfile", "/app/cert/key.pem", "--certfile", "/app/cert/cert.pem", "--access-logfile", "-", "--error-logfile", "-"]
