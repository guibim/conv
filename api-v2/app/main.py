from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routes.convert import router as convert_router


app = FastAPI(
    title=settings.service_name,
    description="Hardened file conversion API for the Conv project.",
    version=settings.version,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(convert_router)


@app.get("/")
def root() -> dict[str, object]:
    return {
        "service": settings.service_name,
        "version": settings.version,
        "docs": "/docs",
        "health": "/health",
        "conversions": "/conversions",
    }
