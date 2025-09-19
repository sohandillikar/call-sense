"""
API endpoints for review monitoring and analysis
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from pydantic import BaseModel

from app.core.database import get_db
from app.services.bright_data_client import bright_data_client, review_analysis_service
from app.services.vector_search import vector_search_service
from app.services.tigerdata_client import time_series_analysis_service
from app.models.review import CompanyReview, CompetitorReview, ReviewAnalysis

router = APIRouter()


class ReviewScrapingRequest(BaseModel):
    business_name: str
    location: str = ""
    platforms: List[str] = ["google", "yelp"]


class ReviewAnalysisRequest(BaseModel):
    company_name: str
    competitor_names: List[str]
    analysis_period_days: int = 30


class ReviewResponse(BaseModel):
    platform: str
    reviewer_name: str
    rating: float
    review_text: str
    sentiment_score: float
    sentiment_label: str
    key_themes: List[str]


@router.post("/scrape-company", response_model=List[ReviewResponse])
async def scrape_company_reviews(
    request: ReviewScrapingRequest,
    db: Session = Depends(get_db)
):
    """Scrape reviews for the company"""
    try:
        all_reviews = []
        
        # Scrape from different platforms
        if "google" in request.platforms:
            google_reviews = await bright_data_client.scrape_google_reviews(
                request.business_name, request.location
            )
            all_reviews.extend(google_reviews)
        
        if "yelp" in request.platforms:
            yelp_reviews = await bright_data_client.scrape_yelp_reviews(
                request.business_name, request.location
            )
            all_reviews.extend(yelp_reviews)
        
        # Process and analyze reviews
        processed_reviews = []
        for review in all_reviews:
            # Analyze sentiment
            sentiment_analysis = await review_analysis_service.analyze_review_sentiment(
                review.get("review_text", "")
            )
            
            # Extract themes
            themes = await review_analysis_service.extract_review_themes(
                review.get("review_text", "")
            )
            
            # Store in database
            review_record = CompanyReview(
                review_id=f"{review.get('platform', '')}_{review.get('reviewer_name', '')}_{review.get('review_date', '')}",
                platform=review.get("platform", ""),
                reviewer_name=review.get("reviewer_name", ""),
                rating=review.get("rating", 0),
                review_text=review.get("review_text", ""),
                sentiment_score=sentiment_analysis["sentiment_score"],
                sentiment_label=sentiment_analysis["sentiment_label"],
                key_themes=themes,
                is_verified=review.get("is_verified", False),
                response_text=review.get("business_response", "")
            )
            
            db.add(review_record)
            
            # Store in vector search
            review_metadata = {
                "platform": review.get("platform", ""),
                "rating": review.get("rating", 0),
                "created_at": review.get("scraped_at", ""),
                "is_verified": review.get("is_verified", False)
            }
            
            review_analysis = {
                "sentiment_analysis": sentiment_analysis,
                "themes": themes
            }
            
            await vector_search_service.store_review_insight(
                review.get("review_text", ""), review_analysis, review_metadata
            )
            
            processed_reviews.append(ReviewResponse(
                platform=review.get("platform", ""),
                reviewer_name=review.get("reviewer_name", ""),
                rating=review.get("rating", 0),
                review_text=review.get("review_text", ""),
                sentiment_score=sentiment_analysis["sentiment_score"],
                sentiment_label=sentiment_analysis["sentiment_label"],
                key_themes=themes
            ))
        
        db.commit()
        
        # Store in time-series data
        await time_series_analysis_service.store_review_sentiment_trends(
            request.business_name, processed_reviews
        )
        
        return processed_reviews
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/scrape-competitor", response_model=List[ReviewResponse])
async def scrape_competitor_reviews(
    request: ReviewScrapingRequest,
    db: Session = Depends(get_db)
):
    """Scrape reviews for competitors"""
    try:
        all_reviews = []
        
        # Scrape from different platforms
        if "google" in request.platforms:
            google_reviews = await bright_data_client.scrape_google_reviews(
                request.business_name, request.location
            )
            all_reviews.extend(google_reviews)
        
        if "yelp" in request.platforms:
            yelp_reviews = await bright_data_client.scrape_yelp_reviews(
                request.business_name, request.location
            )
            all_reviews.extend(yelp_reviews)
        
        # Process and analyze reviews
        processed_reviews = []
        for review in all_reviews:
            # Analyze sentiment
            sentiment_analysis = await review_analysis_service.analyze_review_sentiment(
                review.get("review_text", "")
            )
            
            # Extract themes
            themes = await review_analysis_service.extract_review_themes(
                review.get("review_text", "")
            )
            
            # Store in database
            review_record = CompetitorReview(
                review_id=f"{review.get('platform', '')}_{review.get('reviewer_name', '')}_{review.get('review_date', '')}",
                competitor_name=request.business_name,
                platform=review.get("platform", ""),
                reviewer_name=review.get("reviewer_name", ""),
                rating=review.get("rating", 0),
                review_text=review.get("review_text", ""),
                sentiment_score=sentiment_analysis["sentiment_score"],
                sentiment_label=sentiment_analysis["sentiment_label"],
                key_themes=themes,
                competitive_insights=themes  # Use themes as competitive insights for now
            )
            
            db.add(review_record)
            
            processed_reviews.append(ReviewResponse(
                platform=review.get("platform", ""),
                reviewer_name=review.get("reviewer_name", ""),
                rating=review.get("rating", 0),
                review_text=review.get("review_text", ""),
                sentiment_score=sentiment_analysis["sentiment_score"],
                sentiment_label=sentiment_analysis["sentiment_label"],
                key_themes=themes
            ))
        
        db.commit()
        
        return processed_reviews
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze-competitive")
async def analyze_competitive_reviews(
    request: ReviewAnalysisRequest,
    db: Session = Depends(get_db)
):
    """Analyze competitive position based on reviews"""
    try:
        # Get company reviews
        company_reviews = db.query(CompanyReview).filter(
            CompanyReview.platform.in_(["google", "yelp"])
        ).all()
        
        # Get competitor reviews
        competitor_reviews = db.query(CompetitorReview).filter(
            CompetitorReview.competitor_name.in_(request.competitor_names)
        ).all()
        
        # Convert to format expected by analysis service
        company_review_data = [
            {
                "rating": review.rating,
                "sentiment_score": review.sentiment_score,
                "review_text": review.review_text
            }
            for review in company_reviews
        ]
        
        competitor_review_data = [
            {
                "rating": review.rating,
                "sentiment_score": review.sentiment_score,
                "review_text": review.review_text
            }
            for review in competitor_reviews
        ]
        
        # Generate competitive insights
        competitive_insights = await review_analysis_service.generate_competitive_insights(
            company_review_data, competitor_review_data
        )
        
        # Store analysis in database
        analysis_record = ReviewAnalysis(
            company_name=request.company_name,
            analysis_type="competitive",
            platform="all",
            total_reviews=len(company_reviews) + len(competitor_reviews),
            average_rating=competitive_insights["company_performance"]["average_rating"],
            sentiment_distribution={
                "company": competitive_insights["company_performance"],
                "competitors": competitive_insights["competitor_performance"]
            },
            competitive_position=competitive_insights["competitive_position"]
        )
        
        db.add(analysis_record)
        db.commit()
        
        return competitive_insights
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/company/{company_name}")
async def get_company_reviews(
    company_name: str,
    platform: str = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get company reviews with optional filtering"""
    try:
        query = db.query(CompanyReview)
        
        if platform:
            query = query.filter(CompanyReview.platform == platform)
        
        reviews = query.offset(skip).limit(limit).all()
        
        return [
            {
                "review_id": review.review_id,
                "platform": review.platform,
                "reviewer_name": review.reviewer_name,
                "rating": review.rating,
                "review_text": review.review_text,
                "sentiment_score": review.sentiment_score,
                "sentiment_label": review.sentiment_label,
                "key_themes": review.key_themes,
                "created_at": review.created_at
            }
            for review in reviews
        ]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/competitor/{competitor_name}")
async def get_competitor_reviews(
    competitor_name: str,
    platform: str = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get competitor reviews with optional filtering"""
    try:
        query = db.query(CompetitorReview).filter(
            CompetitorReview.competitor_name == competitor_name
        )
        
        if platform:
            query = query.filter(CompetitorReview.platform == platform)
        
        reviews = query.offset(skip).limit(limit).all()
        
        return [
            {
                "review_id": review.review_id,
                "platform": review.platform,
                "reviewer_name": review.reviewer_name,
                "rating": review.rating,
                "review_text": review.review_text,
                "sentiment_score": review.sentiment_score,
                "sentiment_label": review.sentiment_label,
                "key_themes": review.key_themes,
                "competitive_insights": review.competitive_insights,
                "created_at": review.created_at
            }
            for review in reviews
        ]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/similar/{review_text}")
async def find_similar_reviews(review_text: str, limit: int = 5):
    """Find similar reviews using vector search"""
    try:
        similar_reviews = await vector_search_service.find_similar_reviews(review_text, limit)
        return similar_reviews
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
