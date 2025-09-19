"""
API endpoints for competitor monitoring and pricing analysis
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from pydantic import BaseModel
from datetime import datetime

from app.core.database import get_db
from app.services.bright_data_client import bright_data_client
from app.services.tigerdata_client import time_series_analysis_service
from app.models.competitor_data import CompetitorData, PricingData, MarketAnalysis, CompetitorAlert

router = APIRouter()


class CompetitorMonitoringRequest(BaseModel):
    competitor_name: str
    website_url: str
    industry: str
    market_position: str = "competitive"


class PricingScrapingRequest(BaseModel):
    competitor_name: str
    product_category: str = ""


class MarketAnalysisRequest(BaseModel):
    product_category: str
    analysis_period_days: int = 30


class CompetitorResponse(BaseModel):
    competitor_name: str
    website_url: str
    industry: str
    market_position: str
    is_active: bool


class PricingResponse(BaseModel):
    competitor_name: str
    product_name: str
    product_category: str
    price: float
    currency: str
    availability: str
    scraped_at: str


@router.post("/add", response_model=CompetitorResponse)
async def add_competitor(
    request: CompetitorMonitoringRequest,
    db: Session = Depends(get_db)
):
    """Add a new competitor to monitor"""
    try:
        # Check if competitor already exists (exact match first)
        existing = db.query(CompetitorData).filter(
            CompetitorData.competitor_name == request.competitor_name
        ).first()
        
        if existing:
            raise HTTPException(
                status_code=400, 
                detail=f"Competitor '{request.competitor_name}' already exists. Please choose a different name or use the existing competitor."
            )
        
        # Create new competitor record
        competitor = CompetitorData(
            competitor_name=request.competitor_name,
            website_url=request.website_url,
            industry=request.industry,
            market_position=request.market_position
        )
        
        db.add(competitor)
        db.commit()
        
        return CompetitorResponse(
            competitor_name=competitor.competitor_name,
            website_url=competitor.website_url,
            industry=competitor.industry,
            market_position=competitor.market_position,
            is_active=competitor.is_active
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/")
async def list_competitors(
    skip: int = 0,
    limit: int = 100,
    industry: str = None,
    db: Session = Depends(get_db)
):
    """List all competitors with optional filtering"""
    try:
        query = db.query(CompetitorData).filter(CompetitorData.is_active == True)
        
        if industry:
            query = query.filter(CompetitorData.industry == industry)
        
        competitors = query.offset(skip).limit(limit).all()
        
        return [
            {
                "id": competitor.id,
                "competitor_name": competitor.competitor_name,
                "website_url": competitor.website_url,
                "industry": competitor.industry,
                "market_position": competitor.market_position,
                "created_at": competitor.created_at
            }
            for competitor in competitors
        ]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/scrape-pricing", response_model=List[PricingResponse])
async def scrape_competitor_pricing(
    request: PricingScrapingRequest,
    db: Session = Depends(get_db)
):
    """Scrape competitor pricing information"""
    try:
        # Scrape pricing data using Bright Data
        pricing_data = await bright_data_client.scrape_competitor_pricing(
            request.competitor_name, request.product_category
        )
        
        # Store pricing data in database
        stored_pricing = []
        for item in pricing_data:
            pricing_record = PricingData(
                competitor_name=request.competitor_name,
                product_name=item.get("product_name", ""),
                product_category=item.get("product_category", request.product_category),
                price=item.get("price", 0),
                currency=item.get("currency", "USD"),
                availability=item.get("availability", "unknown"),
                data_source="web_scraping",
                confidence_score=0.8  # Default confidence score
            )
            
            db.add(pricing_record)
            stored_pricing.append(PricingResponse(
                competitor_name=request.competitor_name,
                product_name=item.get("product_name", ""),
                product_category=item.get("product_category", request.product_category),
                price=item.get("price", 0),
                currency=item.get("currency", "USD"),
                availability=item.get("availability", "unknown"),
                scraped_at=item.get("scraped_at", "")
            ))
        
        db.commit()
        
        # Store in time-series data
        await time_series_analysis_service.store_competitor_pricing_trends(
            request.competitor_name, pricing_data
        )
        
        return stored_pricing
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/pricing/{competitor_name}")
async def get_competitor_pricing(
    competitor_name: str,
    product_category: str = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get competitor pricing data"""
    try:
        query = db.query(PricingData).filter(
            PricingData.competitor_name == competitor_name
        )
        
        if product_category:
            query = query.filter(PricingData.product_category == product_category)
        
        pricing_data = query.offset(skip).limit(limit).all()
        
        return [
            {
                "id": pricing.id,
                "competitor_name": pricing.competitor_name,
                "product_name": pricing.product_name,
                "product_category": pricing.product_category,
                "price": pricing.price,
                "currency": pricing.currency,
                "availability": pricing.availability,
                "data_source": pricing.data_source,
                "confidence_score": pricing.confidence_score,
                "scraped_at": pricing.scraped_at
            }
            for pricing in pricing_data
        ]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze-market")
async def analyze_market(
    request: MarketAnalysisRequest,
    db: Session = Depends(get_db)
):
    """Analyze market trends and competitive landscape"""
    try:
        # Get pricing data for the product category
        pricing_data = db.query(PricingData).filter(
            PricingData.product_category == request.product_category
        ).all()
        
        if not pricing_data:
            raise HTTPException(status_code=404, detail="No pricing data found for this category")
        
        # Calculate market metrics
        prices = [p.price for p in pricing_data if p.price > 0]
        competitors = list(set([p.competitor_name for p in pricing_data]))
        
        market_size = len(pricing_data) * 1000  # Placeholder calculation
        market_growth_rate = 0.05  # Placeholder - would be calculated from historical data
        
        average_price = sum(prices) / len(prices) if prices else 0
        price_range = {
            "min": min(prices) if prices else 0,
            "max": max(prices) if prices else 0
        }
        
        # Calculate market share distribution (placeholder)
        market_share_distribution = {}
        for competitor in competitors:
            competitor_prices = [p.price for p in pricing_data if p.competitor_name == competitor and p.price > 0]
            if competitor_prices:
                avg_competitor_price = sum(competitor_prices) / len(competitor_prices)
                market_share_distribution[competitor] = {
                    "average_price": avg_competitor_price,
                    "product_count": len(competitor_prices),
                    "market_share": len(competitor_prices) / len(pricing_data) * 100
                }
        
        # Generate key trends and recommendations
        key_trends = [
            f"Average market price: ${average_price:.2f}",
            f"Price range: ${price_range['min']:.2f} - ${price_range['max']:.2f}",
            f"Number of competitors: {len(competitors)}"
        ]
        
        recommendations = [
            "Monitor competitor pricing changes weekly",
            "Consider dynamic pricing strategies",
            "Focus on value proposition differentiation"
        ]
        
        # Store market analysis
        analysis_record = MarketAnalysis(
            analysis_date=datetime.now(),
            product_category=request.product_category,
            market_size=market_size,
            market_growth_rate=market_growth_rate,
            competitor_count=len(competitors),
            average_price=average_price,
            price_range=price_range,
            market_share_distribution=market_share_distribution,
            key_trends=key_trends,
            recommendations=recommendations
        )
        
        db.add(analysis_record)
        db.commit()
        
        return {
            "product_category": request.product_category,
            "analysis_date": analysis_record.analysis_date.isoformat(),
            "market_size": market_size,
            "market_growth_rate": market_growth_rate,
            "competitor_count": len(competitors),
            "average_price": average_price,
            "price_range": price_range,
            "market_share_distribution": market_share_distribution,
            "key_trends": key_trends,
            "recommendations": recommendations
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/alerts")
async def get_competitor_alerts(
    severity: str = None,
    is_read: bool = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get competitor alerts and notifications"""
    try:
        query = db.query(CompetitorAlert)
        
        if severity:
            query = query.filter(CompetitorAlert.severity == severity)
        
        if is_read is not None:
            query = query.filter(CompetitorAlert.is_read == is_read)
        
        alerts = query.order_by(CompetitorAlert.created_at.desc()).offset(skip).limit(limit).all()
        
        return [
            {
                "id": alert.id,
                "competitor_name": alert.competitor_name,
                "alert_type": alert.alert_type,
                "alert_title": alert.alert_title,
                "alert_description": alert.alert_description,
                "severity": alert.severity,
                "is_read": alert.is_read,
                "alert_metadata": alert.alert_metadata,
                "created_at": alert.created_at
            }
            for alert in alerts
        ]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/alerts/{alert_id}/mark-read")
async def mark_alert_read(alert_id: int, db: Session = Depends(get_db)):
    """Mark a competitor alert as read"""
    try:
        alert = db.query(CompetitorAlert).filter(CompetitorAlert.id == alert_id).first()
        
        if not alert:
            raise HTTPException(status_code=404, detail="Alert not found")
        
        alert.is_read = True
        db.commit()
        
        return {"message": "Alert marked as read"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/trends/{competitor_name}")
async def get_competitor_trends(competitor_name: str, days: int = 30):
    """Get competitor pricing trends over time"""
    try:
        trends = await time_series_analysis_service.analyze_pricing_trends(competitor_name, days)
        return trends
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
