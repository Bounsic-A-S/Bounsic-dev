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
COPY ./bounsic-back/cert/key.pem /app/cert/key.pem
COPY ./bounsic-back/cert/cert.pem /app/cert/cert.pem

# Puerto expuesto
EXPOSE 443

# Comando de inicio del servidor FastAPI en HTTPS
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "443", "--ssl-keyfile", "/app/cert/key.pem", "--ssl-certfile", "/app/cert/cert.pem", "--access-log", "--log-level", "debug"]
