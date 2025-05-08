# Imagen base de Python
FROM python:3.11.9-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar archivos necesarios
COPY . .

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto que usará la aplicación
EXPOSE 4000

# Comando de inicio utilizando Hypercorn
CMD ["python", "hypercorn_app.py"]
