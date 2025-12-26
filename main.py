from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.v1.api import router as api_v1_router

app = FastAPI(
    title="StudyAbroadAi - Your AI Big Bro for Studying Abroad",
    description="A personalized AI advisor for Bangladeshi and global students planning to study abroad.",
    version="0.1.0",
    contact={"name": "StudyAbroadAi Team"},
    license_info={"name": "MIT"},
)

# CORS Configuration
origins = [
    "http://localhost:3000",  # Next.js local
    "https://studyabroadai.vercel.app", # Vercel production
    "*", # Allow all for now (development)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_v1_router)

@app.get("/", tags=["Root"])
def home():
    return {
        "message": "StudyAbroadAi backend is LIVE! 🚀",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health"
    }

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy", "service": "StudyAbroadAi backend"}