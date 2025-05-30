from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router as api_router
from app.core.config import settings
from app.models.database import Base
from app.db.database import engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Legal Assistant AI aPI",
    description="API for legal assistant AI application",
    version="1.0.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to the legal assistant AI API"}
