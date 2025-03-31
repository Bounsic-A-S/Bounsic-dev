from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from app.services import pregunta_respuesta
from app.provider.mongo_db import db

router = APIRouter()

@router.get("/")
async def home():
    try:
        print("Conexión exitosa a MongoDB:", db.list_collection_names())
    except Exception as e:
        print("Error conectando a MongoDB:", e)
    return {"message": "¡Hola, Bounsic-back está funcionando!"}

@router.post("/ask")
async def ask(request: Request):
    data = await request.json()  # Obtener el JSON de la solicitud
    question = data.get("question", "")

    response = pregunta_respuesta(question)  # Llama a la función del modelo
    return JSONResponse(content=response)

