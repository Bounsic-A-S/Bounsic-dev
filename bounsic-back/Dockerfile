# Etapa 1: Construcción
FROM python:3.11-slim AS builder

# Evitar problemas de encoding
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Crear directorio de trabajo
WORKDIR /

# Instalar dependencias del sistema necesarias para paquetes como numpy, pandas, etc.
RUN apt-get update && apt-get install -y \
    ffmpeg \
    gcc \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copiar solo requirements y preinstalar (esto aprovecha el cache de Docker)
COPY ./requirements.txt .

# Instalar dependencias en una carpeta separada
RUN pip install --upgrade pip \
    && pip install --prefix=/install -r requirements.txt


# Etapa 2: Imagen final más liviana
FROM python:3.11-slim

# Crear directorio de trabajo
WORKDIR /

# Instalar ffmpeg en la etapa final
RUN apt-get update && apt-get install -y ffmpeg && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copiar las dependencias instaladas desde la etapa anterior
COPY --from=builder /install /usr/local

# Copiar el resto del código de la aplicación
COPY . .

# Exponer el puerto por defecto de FastAPI
EXPOSE 8000

# Comando para ejecutar la app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

