"""
Main API routes for the AI Business Assistant
"""
from fastapi import APIRouter
from app.api.endpoints import calls, reviews, competitors, insights, analytics

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(calls.router, prefix="/calls", tags=["calls"])
api_router.include_router(reviews.router, prefix="/reviews", tags=["reviews"])
api_router.include_router(competitors.router, prefix="/competitors", tags=["competitors"])
api_router.include_router(insights.router, prefix="/insights", tags=["insights"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
