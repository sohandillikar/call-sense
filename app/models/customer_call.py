"""
Customer call and voicemail models
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, JSON
from sqlalchemy.sql import func
from app.core.database import Base


class CustomerCall(Base):
    """Model for storing customer call transcriptions and insights"""
    
    __tablename__ = "customer_calls"
    
    id = Column(Integer, primary_key=True, index=True)
    call_id = Column(String, unique=True, index=True)
    customer_phone = Column(String)
    call_type = Column(String)  # 'incoming', 'outgoing', 'voicemail'
    duration_seconds = Column(Float)
    transcription = Column(Text)
    sentiment_score = Column(Float)  # -1 to 1
    sentiment_label = Column(String)  # 'positive', 'negative', 'neutral'
    key_topics = Column(JSON)  # List of extracted topics
    action_items = Column(JSON)  # List of action items
    priority_score = Column(Float)  # 0 to 1
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class CallInsight(Base):
    """Model for storing AI-generated insights from calls"""
    
    __tablename__ = "call_insights"
    
    id = Column(Integer, primary_key=True, index=True)
    call_id = Column(String, index=True)
    insight_type = Column(String)  # 'customer_satisfaction', 'product_feedback', 'complaint', etc.
    insight_text = Column(Text)
    confidence_score = Column(Float)  # 0 to 1
    suggested_actions = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
