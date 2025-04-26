from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from streeming import router  # Asegúrate que el nombre coincida con tu archivo
from config import ALLOWED_ORIGINS
import uvicorn

app = FastAPI()

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["Range", "Origin", "Content-Type"],
    expose_headers=["Content-Range", "Accept-Ranges", "Content-Length"]
)

app.include_router(router)

if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=4000)