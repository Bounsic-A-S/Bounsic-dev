# Usa una imagen base oficial de Python, con imagen reducida
FROM python:3.11-slim

# Establece variables de entorno para evitar mensajes interactivos
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Establece el directorio de trabajo
WORKDIR /app

# Instala dependencias del sistema necesarias para compilar algunas bibliotecas
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc libpq-dev curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copia solo los archivos necesarios para instalar dependencias
COPY requirements.txt .

# Instala dependencias del proyecto
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del proyecto
COPY . .

# Exponer el puerto usado por Hypercorn
EXPOSE 4000

# Comando para correr el servidor
CMD ["hypercorn", "main:app", "--bind", "0.0.0.0:4000"]
