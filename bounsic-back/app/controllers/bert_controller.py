from app.services import Bert_service
from fastapi import HTTPException

class Bert_controller:
    @staticmethod
    async def bert_request(question : str):
        if not question:
            raise HTTPException(status_code=400, detail="The 'question' field is required")
        return Bert_service.pregunta_respuesta(question)