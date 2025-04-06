import os
from dotenv import load_dotenv
from pathlib import Path
from pymongo import MongoClient
import certifi

dotenv_path = Path(__file__).resolve().parent.parent.parent / "env" / ".env.dev"
if not load_dotenv(dotenv_path):
    print(f"⚠️ No se pudo cargar el archivo {dotenv_path}")

MONGO_CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING")
MONGO_DATABASE_NAME = os.getenv("MONGO_DATABASE_NAME")

client = MongoClient(MONGO_CONNECTION_STRING, tlsCAFile=certifi.where())
db = client[MONGO_DATABASE_NAME]

