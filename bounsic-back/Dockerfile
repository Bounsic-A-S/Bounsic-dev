# Etapa 1: Builder
FROM python:3.11-alpine AS builder

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Instala dependencias del sistema + ffmpeg
RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    build-base \
    libpq \
    ffmpeg 

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --prefix=/install -r requirements.txt

# Etapa final
FROM python:3.11-alpine

WORKDIR /

# Instala ffmpeg y librerías necesarias también en la etapa final
RUN apk add --no-cache ffmpeg

# Copia dependencias de Python instaladas desde builder
COPY --from=builder /install /usr/local

# Copia tu código fuente
COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
