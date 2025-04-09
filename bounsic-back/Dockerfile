# Etapa 1: Builder
FROM python:3.11-slim AS builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Instala librerías necesarias para compilar y ffmpeg
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    ffmpeg \
    wget \
    curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./

# Instala las dependencias con cache off y las guarda en /install
RUN pip install --upgrade pip && pip install --no-cache-dir --prefix=/install -r requirements.txt

# Instala playwright y navegadores
RUN pip install --no-cache-dir playwright && playwright install chromium

# Etapa final
FROM python:3.11-slim

WORKDIR /app

# Instala librerías mínimas necesarias para Chromium y ffmpeg
RUN apt-get update && apt-get install -y \
    libnss3 libatk-bridge2.0-0 libgtk-3-0 libdrm2 libxshmfence1 \
    libasound2 libxss1 libgbm1 fonts-liberation xdg-utils ffmpeg \
    ca-certificates wget curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copia solo las dependencias de Python ya instaladas
COPY --from=builder /install /usr/local

# Copia el código fuente
COPY . .

# Exponer el puerto
EXPOSE 8000

# Comando de inicio
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
