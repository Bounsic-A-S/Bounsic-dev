
# Iniciar la aplicación con Uvicorn en segundo plano
cd /app
echo "Iniciando aplicación con Uvicorn..."
uvicorn main:app --host 0.0.0.0 --port 8000 --log-level info &

# Esperar un momento para que Uvicorn inicie
sleep 3

# Iniciar Nginx en primer plano
echo "Iniciando Nginx..."
nginx -g "daemon off;"