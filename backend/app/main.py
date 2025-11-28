from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import analyze
from app.config import settings

app = FastAPI(
    title="Databricks Engagement Intelligence API",
    description="API for analyzing customer engagements using local LLMs",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, specify frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analyze.router, prefix="/api", tags=["Analysis"])

@app.get("/")
async def root():
    return {"message": "Databricks Engagement Intelligence API is running"}

@app.get("/health")
async def health():
    return {"status": "ok", "mode": settings.MODEL_MODE}
