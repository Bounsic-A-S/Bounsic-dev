# Usa una imagen base oficial de Python
FROM python:3.11-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos del proyecto al contenedor
COPY . .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Verifica las dependencias instaladas
RUN pip freeze

# Instala el servidor SSH
RUN apt-get update && apt-get install -y openssh-server

# Configura SSH
RUN mkdir /var/run/sshd \
    && echo 'PermitRootLogin yes' >> /etc/ssh/sshd_config \
    && echo 'PasswordAuthentication yes' >> /etc/ssh/sshd_config \
    && echo 'root:password123' | chpasswd  # Cambia la contraseña por una segura

# Exponer puertos: 
# 4000 para Hypercorn (tu aplicación)
# 22 para SSH
EXPOSE 4000 22

# Comando para iniciar SSH y Hypercorn
CMD service ssh start && hypercorn main:app --bind 0.0.0.0:4000
