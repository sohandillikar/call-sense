"""
Review models for company and competitor reviews
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, JSON, Boolean
from sqlalchemy.sql import func
from app.core.database import Base


class CompanyReview(Base):
    """Model for storing company reviews"""
    
    __tablename__ = "company_reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    review_id = Column(String, unique=True, index=True)
    platform = Column(String)  # 'google', 'yelp', 'facebook', etc.
    reviewer_name = Column(String)
    rating = Column(Float)  # 1-5 stars
    review_text = Column(Text)
    sentiment_score = Column(Float)  # -1 to 1
    sentiment_label = Column(String)
    key_themes = Column(JSON)  # List of themes/topics
    is_verified = Column(Boolean, default=False)
    response_text = Column(Text)  # Company response if any
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class CompetitorReview(Base):
    """Model for storing competitor reviews"""
    
    __tablename__ = "competitor_reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    review_id = Column(String, unique=True, index=True)
    competitor_name = Column(String, index=True)
    platform = Column(String)
    reviewer_name = Column(String)
    rating = Column(Float)
    review_text = Column(Text)
    sentiment_score = Column(Float)
    sentiment_label = Column(String)
    key_themes = Column(JSON)
    competitive_insights = Column(JSON)  # AI-extracted competitive insights
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class ReviewAnalysis(Base):
    """Model for storing aggregated review analysis"""
    
    __tablename__ = "review_analysis"
    
    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String, index=True)
    analysis_type = Column(String)  # 'company', 'competitor'
    platform = Column(String)
    period_start = Column(DateTime)
    period_end = Column(DateTime)
    total_reviews = Column(Integer)
    average_rating = Column(Float)
    sentiment_distribution = Column(JSON)  # Distribution of sentiment scores
    top_themes = Column(JSON)  # Most common themes
    trend_analysis = Column(JSON)  # Rating/sentiment trends over time
    competitive_position = Column(String)  # 'leading', 'competitive', 'lagging'
    created_at = Column(DateTime(timezone=True), server_default=func.now())
