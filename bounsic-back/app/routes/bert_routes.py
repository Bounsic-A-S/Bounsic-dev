from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from app.controllers import bert_request

router = APIRouter()

@router.post("/ask")
async def ask(request: Request):
    try:
        data = await request.json()
        question = data.get("question","")
            
        response = bert_request(question)
        return JSONResponse(content={"response": response})
    
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": "Internal Server Error", "detail": str(e)}
        )

