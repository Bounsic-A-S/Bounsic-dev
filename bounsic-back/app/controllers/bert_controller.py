from app.services import pregunta_respuesta
from fastapi import HTTPException

def bert_request(question : str):
    if not question:
        raise HTTPException(status_code=400, detail="The 'question' field is required")
    return pregunta_respuesta(question)