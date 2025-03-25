FROM nginx:alpine

# Crear el directorio sites-available
RUN mkdir /etc/nginx/sites-available

# Copiar el archivo de configuración del sitio (default) a sites-available
COPY default /etc/nginx/sites-available/

# Copiar el archivo nginx.conf modificado
COPY nginx.conf /etc/nginx/

# Copiar los archivos de la aplicación Angular construida.
COPY dist/bounsic-front/browser /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]