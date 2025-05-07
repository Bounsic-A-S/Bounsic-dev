# Usa una imagen base oficial de Python
FROM python:3.11-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos del proyecto al contenedor
COPY . .

# Instala las dependencias del sistema que pueden ser necesarias para las dependencias de Python
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Crea un entorno virtual
RUN python -m venv venv

# Instala las dependencias dentro del entorno virtual
RUN venv/bin/pip install --no-cache-dir -r requirements.txt

# Establece la variable de entorno para usar el venv
ENV PATH="/app/venv/bin:$PATH"

# Exponer el puerto por defecto de Hypercorn
EXPOSE 4000

# Comando para correr el servidor con Hypercorn dentro del venv
CMD ["hypercorn", "hypercorn_server:app", "--bind", "0.0.0.0:8000"]
