"""
Competitor monitoring and pricing models
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, JSON, Boolean
from sqlalchemy.sql import func
from app.core.database import Base


class CompetitorData(Base):
    """Model for storing competitor information and monitoring data"""
    
    __tablename__ = "competitor_data"
    
    id = Column(Integer, primary_key=True, index=True)
    competitor_name = Column(String, index=True)
    website_url = Column(String)
    industry = Column(String)
    market_position = Column(String)  # 'leader', 'challenger', 'follower', 'niche'
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class PricingData(Base):
    """Model for storing competitor pricing information"""
    
    __tablename__ = "pricing_data"
    
    id = Column(Integer, primary_key=True, index=True)
    competitor_name = Column(String, index=True)
    product_name = Column(String)
    product_category = Column(String)
    price = Column(Float)
    currency = Column(String, default="USD")
    price_type = Column(String)  # 'base', 'sale', 'subscription', etc.
    availability = Column(String)  # 'in_stock', 'out_of_stock', 'limited'
    data_source = Column(String)  # 'web_scraping', 'api', 'manual'
    confidence_score = Column(Float)  # 0 to 1
    scraped_at = Column(DateTime(timezone=True), server_default=func.now())


class MarketAnalysis(Base):
    """Model for storing market analysis and insights"""
    
    __tablename__ = "market_analysis"
    
    id = Column(Integer, primary_key=True, index=True)
    analysis_date = Column(DateTime, index=True)
    product_category = Column(String, index=True)
    market_size = Column(Float)
    market_growth_rate = Column(Float)
    competitor_count = Column(Integer)
    average_price = Column(Float)
    price_range = Column(JSON)  # Min and max prices
    market_share_distribution = Column(JSON)  # Competitor market shares
    key_trends = Column(JSON)  # Market trends and insights
    recommendations = Column(JSON)  # AI-generated recommendations
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class CompetitorAlert(Base):
    """Model for storing competitor alerts and notifications"""
    
    __tablename__ = "competitor_alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    competitor_name = Column(String, index=True)
    alert_type = Column(String)  # 'price_change', 'new_product', 'promotion', etc.
    alert_title = Column(String)
    alert_description = Column(Text)
    severity = Column(String)  # 'low', 'medium', 'high', 'critical'
    is_read = Column(Boolean, default=False)
    alert_metadata = Column(JSON)  # Additional alert data
    created_at = Column(DateTime(timezone=True), server_default=func.now())
