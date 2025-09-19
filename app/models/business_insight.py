"""
Business insights and analytics models
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, JSON, Boolean
from sqlalchemy.sql import func
from app.core.database import Base


class BusinessInsight(Base):
    """Model for storing AI-generated business insights"""
    
    __tablename__ = "business_insights"
    
    id = Column(Integer, primary_key=True, index=True)
    insight_type = Column(String, index=True)  # 'customer_satisfaction', 'market_trend', 'competitor_analysis', etc.
    title = Column(String)
    description = Column(Text)
    confidence_score = Column(Float)  # 0 to 1
    impact_score = Column(Float)  # 0 to 1
    priority = Column(String)  # 'low', 'medium', 'high', 'critical'
    category = Column(String)  # 'customer', 'competitor', 'market', 'financial'
    data_sources = Column(JSON)  # List of data sources used
    recommendations = Column(JSON)  # List of actionable recommendations
    metrics = Column(JSON)  # Related metrics and KPIs
    is_archived = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class TimeSeriesData(Base):
    """Model for storing time-series data for analytics"""
    
    __tablename__ = "time_series_data"
    
    id = Column(Integer, primary_key=True, index=True)
    metric_name = Column(String, index=True)  # 'customer_satisfaction', 'competitor_price', etc.
    metric_category = Column(String)  # 'customer', 'competitor', 'financial', 'market'
    value = Column(Float)
    unit = Column(String)  # 'rating', 'price', 'percentage', etc.
    timestamp = Column(DateTime, index=True)
    data_metadata = Column(JSON)  # Additional context data
    data_source = Column(String)  # Source of the data
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class DashboardWidget(Base):
    """Model for storing dashboard widget configurations"""
    
    __tablename__ = "dashboard_widgets"
    
    id = Column(Integer, primary_key=True, index=True)
    widget_name = Column(String, unique=True)
    widget_type = Column(String)  # 'chart', 'metric', 'table', 'alert'
    title = Column(String)
    description = Column(Text)
    configuration = Column(JSON)  # Widget-specific configuration
    data_query = Column(JSON)  # Query configuration for data
    refresh_interval = Column(Integer)  # Seconds between refreshes
    is_active = Column(Boolean, default=True)
    position_x = Column(Integer)
    position_y = Column(Integer)
    width = Column(Integer)
    height = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class AlertRule(Base):
    """Model for storing alert rules and thresholds"""
    
    __tablename__ = "alert_rules"
    
    id = Column(Integer, primary_key=True, index=True)
    rule_name = Column(String, unique=True)
    metric_name = Column(String, index=True)
    condition = Column(String)  # 'greater_than', 'less_than', 'equals', 'change_percentage'
    threshold_value = Column(Float)
    time_window = Column(Integer)  # Minutes to look back
    severity = Column(String)  # 'low', 'medium', 'high', 'critical'
    is_active = Column(Boolean, default=True)
    notification_channels = Column(JSON)  # Email, SMS, webhook, etc.
    last_triggered = Column(DateTime)
    trigger_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
