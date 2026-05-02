"""
Smart Valuer – FastAPI application entry point.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.analytics import router as analytics_router
from app.api.predict import router as predict_router

app = FastAPI(
    title="Smart Valuer – Real Estate Analytics API",
    description=(
        "Backend API for the Smart Valuer platform. "
        "Provides property price predictions and analytics for the Kenyan real estate market."
    ),
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ---------------------------------------------------------------------------
# CORS – allow the Next.js dev server and any production domain
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",   # Next.js dev server
        "https://smart-valuer.vercel.app",  # example production domain
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------
app.include_router(predict_router)
app.include_router(analytics_router)


@app.get("/", tags=["health"])
def root():
    return {"status": "ok", "service": "Smart Valuer API", "version": "0.1.0"}


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "healthy"}
