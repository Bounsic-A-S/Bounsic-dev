FROM python:3.11-slim

# Instala dependencias necesarias
RUN apt-get update && apt-get install -y \
    curl \
    tar \
    xz-utils \
    && rm -rf /var/lib/apt/lists/*

# Descarga y extrae ffmpeg y ffprobe en /usr/bin
RUN curl -L https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz \
    | tar -xJ && \
    cp ffmpeg-*-static/ffmpeg /usr/bin/ && \
    cp ffmpeg-*-static/ffprobe /usr/bin/ && \
    chmod +x /usr/bin/ffmpeg /usr/bin/ffprobe && \
    rm -rf ffmpeg-*-static

# Verificación
RUN ffmpeg -version && ffprobe -version

# Crea el directorio de trabajo
WORKDIR /

# Copia los archivos y requisitos
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
