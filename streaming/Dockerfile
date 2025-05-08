# Usa una imagen base oficial de Python
FROM python:3.11-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos del proyecto al contenedor
COPY . .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto por defecto de Hypercorn
EXPOSE 4000

# Comando para correr el servidor con Hypercorn
CMD ["hypercorn", "main:app", "--bind", "0.0.0.0:4000"]