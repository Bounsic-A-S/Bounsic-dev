import os
from dotenv import load_dotenv
from pathlib import Path
import httpx
from typing import List

# Cargar las variables de entorno desde el archivo .env
dotenv_path = Path(__file__).resolve().parent.parent.parent / "env" / ".env.dev"
if not load_dotenv(dotenv_path):
    print(f"⚠️ No se pudo cargar el archivo {dotenv_path}")
# Obtener las variables de entorno necesarias
API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")
