from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os

from app.routes import convert

app = FastAPI(
    title="Conv+ API",
    description="Conversor de arquivos",
    version="1.0.0"
)

# CORS acesso do frontend 
origins = [
    os.getenv("ALLOWED_ORIGINS", "*")  # Use "*" para testes, restrinja depois
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rotas de conversão
app.include_router(convert.router)

# Health check
@app.get("/")
def read_root():
    return {"message": "Conv+ backend is running 🚀"}
