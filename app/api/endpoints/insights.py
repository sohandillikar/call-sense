"""
API endpoints for business insights and vector search
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from pydantic import BaseModel
from datetime import datetime

from app.core.database import get_db
from app.services.vector_search import vector_search_service
from app.models.business_insight import BusinessInsight

router = APIRouter()


class InsightRequest(BaseModel):
    insight_type: str
    title: str
    description: str
    confidence_score: float
    impact_score: float
    priority: str
    category: str
    data_sources: List[str]
    recommendations: List[str]
    metrics: Dict[str, Any]


class VectorSearchRequest(BaseModel):
    query_text: str
    search_type: str = "all"  # "all", "issues", "calls", "reviews"
    limit: int = 5


class IssueSolutionRequest(BaseModel):
    issue_text: str
    solution_text: str
    category: str = "general"
    tags: List[str] = []


@router.post("/vector-search")
async def vector_search(request: VectorSearchRequest):
    """Perform vector search across all data types"""
    try:
        if request.search_type == "all":
            # Get comprehensive similarity analysis
            results = await vector_search_service.get_similarity_analysis(request.query_text)
        elif request.search_type == "issues":
            results = await vector_search_service.find_similar_issues(request.query_text, request.limit)
        elif request.search_type == "calls":
            results = await vector_search_service.find_similar_calls(request.query_text, request.limit)
        elif request.search_type == "reviews":
            results = await vector_search_service.find_similar_reviews(request.query_text, request.limit)
        else:
            raise HTTPException(status_code=400, detail="Invalid search_type")
        
        return results
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/store-issue-solution")
async def store_issue_solution(request: IssueSolutionRequest):
    """Store an issue-solution pair for future reference"""
    try:
        metadata = {
            "category": request.category,
            "tags": request.tags,
            "created_at": datetime.now().isoformat()
        }
        
        key = await vector_search_service.store_issue_solution(
            request.issue_text, request.solution_text, metadata
        )
        
        if key:
            return {"message": "Issue-solution stored successfully", "key": key}
        else:
            raise HTTPException(status_code=500, detail="Failed to store issue-solution")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/create-insight")
async def create_business_insight(
    request: InsightRequest,
    db: Session = Depends(get_db)
):
    """Create a new business insight"""
    try:
        insight = BusinessInsight(
            insight_type=request.insight_type,
            title=request.title,
            description=request.description,
            confidence_score=request.confidence_score,
            impact_score=request.impact_score,
            priority=request.priority,
            category=request.category,
            data_sources=request.data_sources,
            recommendations=request.recommendations,
            metrics=request.metrics
        )
        
        db.add(insight)
        db.commit()
        
        return {"message": "Business insight created successfully", "insight_id": insight.id}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/insights")
async def list_business_insights(
    category: str = None,
    priority: str = None,
    is_archived: bool = False,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List business insights with optional filtering"""
    try:
        query = db.query(BusinessInsight).filter(BusinessInsight.is_archived == is_archived)
        
        if category:
            query = query.filter(BusinessInsight.category == category)
        
        if priority:
            query = query.filter(BusinessInsight.priority == priority)
        
        insights = query.order_by(BusinessInsight.created_at.desc()).offset(skip).limit(limit).all()
        
        return [
            {
                "id": insight.id,
                "insight_type": insight.insight_type,
                "title": insight.title,
                "description": insight.description,
                "confidence_score": insight.confidence_score,
                "impact_score": insight.impact_score,
                "priority": insight.priority,
                "category": insight.category,
                "data_sources": insight.data_sources,
                "recommendations": insight.recommendations,
                "metrics": insight.metrics,
                "created_at": insight.created_at,
                "updated_at": insight.updated_at
            }
            for insight in insights
        ]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/insights/{insight_id}")
async def get_business_insight(insight_id: int, db: Session = Depends(get_db)):
    """Get a specific business insight"""
    try:
        insight = db.query(BusinessInsight).filter(BusinessInsight.id == insight_id).first()
        
        if not insight:
            raise HTTPException(status_code=404, detail="Insight not found")
        
        return {
            "id": insight.id,
            "insight_type": insight.insight_type,
            "title": insight.title,
            "description": insight.description,
            "confidence_score": insight.confidence_score,
            "impact_score": insight.impact_score,
            "priority": insight.priority,
            "category": insight.category,
            "data_sources": insight.data_sources,
            "recommendations": insight.recommendations,
            "metrics": insight.metrics,
            "created_at": insight.created_at,
            "updated_at": insight.updated_at
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/insights/{insight_id}/archive")
async def archive_business_insight(insight_id: int, db: Session = Depends(get_db)):
    """Archive a business insight"""
    try:
        insight = db.query(BusinessInsight).filter(BusinessInsight.id == insight_id).first()
        
        if not insight:
            raise HTTPException(status_code=404, detail="Insight not found")
        
        insight.is_archived = True
        db.commit()
        
        return {"message": "Insight archived successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/similar-issues/{query_text}")
async def find_similar_issues(query_text: str, limit: int = 5):
    """Find similar past issues and solutions"""
    try:
        similar_issues = await vector_search_service.find_similar_issues(query_text, limit)
        return similar_issues
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/similar-calls/{query_text}")
async def find_similar_calls(query_text: str, limit: int = 5):
    """Find similar past calls and insights"""
    try:
        similar_calls = await vector_search_service.find_similar_calls(query_text, limit)
        return similar_calls
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/similar-reviews/{query_text}")
async def find_similar_reviews(query_text: str, limit: int = 5):
    """Find similar past reviews and analysis"""
    try:
        similar_reviews = await vector_search_service.find_similar_reviews(query_text, limit)
        return similar_reviews
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/insights/summary")
async def get_insights_summary(db: Session = Depends(get_db)):
    """Get summary of business insights"""
    try:
        # Get insights by category
        categories = db.query(BusinessInsight.category).distinct().all()
        category_summary = {}
        
        for category in categories:
            category_name = category[0]
            insights = db.query(BusinessInsight).filter(
                BusinessInsight.category == category_name,
                BusinessInsight.is_archived == False
            ).all()
            
            category_summary[category_name] = {
                "total_insights": len(insights),
                "high_priority": len([i for i in insights if i.priority == "high"]),
                "average_confidence": sum(i.confidence_score for i in insights) / len(insights) if insights else 0,
                "average_impact": sum(i.impact_score for i in insights) / len(insights) if insights else 0
            }
        
        # Get recent insights
        recent_insights = db.query(BusinessInsight).filter(
            BusinessInsight.is_archived == False
        ).order_by(BusinessInsight.created_at.desc()).limit(5).all()
        
        return {
            "category_summary": category_summary,
            "recent_insights": [
                {
                    "id": insight.id,
                    "title": insight.title,
                    "category": insight.category,
                    "priority": insight.priority,
                    "created_at": insight.created_at
                }
                for insight in recent_insights
            ],
            "total_insights": db.query(BusinessInsight).filter(BusinessInsight.is_archived == False).count()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
