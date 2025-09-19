"""
API endpoints for analytics and time-series data
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from pydantic import BaseModel
from datetime import datetime, timedelta

from app.core.database import get_db
from app.core.config import settings
from app.services.tigerdata_client import time_series_analysis_service, tigerdata_client
from app.models.business_insight import DashboardWidget, AlertRule

router = APIRouter()


class DashboardRequest(BaseModel):
    name: str
    description: str
    widgets: List[Dict[str, Any]]
    refresh_interval: int = 3600


class AlertRuleRequest(BaseModel):
    rule_name: str
    metric_name: str
    condition: str
    threshold_value: float
    time_window: int
    severity: str
    notification_channels: List[str]


@router.get("/sentiment-trends/{company_name}")
async def get_sentiment_trends(company_name: str, days: int = 30):
    """Get sentiment trends over time"""
    try:
        trends = await time_series_analysis_service.analyze_sentiment_trends(company_name, days)
        return trends
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/pricing-trends/{competitor_name}")
async def get_pricing_trends(competitor_name: str, days: int = 30):
    """Get competitor pricing trends over time"""
    try:
        trends = await time_series_analysis_service.analyze_pricing_trends(competitor_name, days)
        return trends
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/customer-satisfaction-trends")
async def get_customer_satisfaction_trends(days: int = 30):
    """Get customer satisfaction trends from call data"""
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        data_points = await tigerdata_client.get_time_series_data(
            "customer_satisfaction_calls", start_date, end_date
        )
        
        if not data_points:
            return {"error": "No data available"}
        
        # Calculate trends
        import pandas as pd
        df = pd.DataFrame(data_points)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['value'] = pd.to_numeric(df['value'])
        
        trend_analysis = {
            "period_days": days,
            "total_data_points": len(data_points),
            "average_satisfaction": df['value'].mean(),
            "satisfaction_range": {
                "min": df['value'].min(),
                "max": df['value'].max()
            },
            "trend_direction": "increasing" if df['value'].iloc[-1] > df['value'].iloc[0] else "decreasing",
            "recent_satisfaction": df['value'].tail(7).mean(),
            "recommendations": [
                "Monitor customer feedback closely" if df['value'].mean() < 0 else "Maintain current satisfaction levels"
            ]
        }
        
        return trend_analysis
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/create-dashboard")
async def create_dashboard(request: DashboardRequest):
    """Create a new analytics dashboard"""
    try:
        dashboard_config = {
            "name": request.name,
            "description": request.description,
            "widgets": request.widgets,
            "refresh_interval": request.refresh_interval,
            "is_public": False
        }
        
        dashboard_id = await tigerdata_client.create_dashboard(dashboard_config)
        
        if dashboard_id:
            return {"message": "Dashboard created successfully", "dashboard_id": dashboard_id}
        else:
            raise HTTPException(status_code=500, detail="Failed to create dashboard")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/dashboard/{dashboard_id}")
async def get_dashboard(dashboard_id: str):
    """Get dashboard data and visualizations"""
    try:
        dashboard_data = await tigerdata_client.get_dashboard_data(dashboard_id)
        return dashboard_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/create-business-dashboard")
async def create_business_dashboard(company_name: str):
    """Create a comprehensive business dashboard"""
    try:
        dashboard_id = await time_series_analysis_service.create_business_dashboard(company_name)
        
        if dashboard_id:
            return {"message": "Business dashboard created successfully", "dashboard_id": dashboard_id}
        else:
            raise HTTPException(status_code=500, detail="Failed to create business dashboard")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/alert-rules")
async def create_alert_rule(
    request: AlertRuleRequest,
    db: Session = Depends(get_db)
):
    """Create a new alert rule"""
    try:
        alert_rule = AlertRule(
            rule_name=request.rule_name,
            metric_name=request.metric_name,
            condition=request.condition,
            threshold_value=request.threshold_value,
            time_window=request.time_window,
            severity=request.severity,
            notification_channels=request.notification_channels
        )
        
        db.add(alert_rule)
        db.commit()
        
        return {"message": "Alert rule created successfully", "rule_id": alert_rule.id}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/alert-rules")
async def list_alert_rules(
    is_active: bool = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List alert rules with optional filtering"""
    try:
        query = db.query(AlertRule)
        
        if is_active is not None:
            query = query.filter(AlertRule.is_active == is_active)
        
        alert_rules = query.offset(skip).limit(limit).all()
        
        return [
            {
                "id": rule.id,
                "rule_name": rule.rule_name,
                "metric_name": rule.metric_name,
                "condition": rule.condition,
                "threshold_value": rule.threshold_value,
                "time_window": rule.time_window,
                "severity": rule.severity,
                "is_active": rule.is_active,
                "notification_channels": rule.notification_channels,
                "last_triggered": rule.last_triggered,
                "trigger_count": rule.trigger_count,
                "created_at": rule.created_at
            }
            for rule in alert_rules
        ]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/metrics/summary")
async def get_metrics_summary(db: Session = Depends(get_db)):
    """Get summary of all metrics and KPIs"""
    try:
        # Since we're using TigerData for time-series data, return a summary
        # that indicates the data is stored in TigerData
        return {
            "message": "Time-series data is stored in TigerData",
            "tigerdata_configured": bool(settings.TIGERDATA_SERVICE_URL),
            "available_metrics": [
                "customer_satisfaction_calls",
                "competitor_pricing_*",
                "review_sentiment_*"
            ],
            "last_updated": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/widgets")
async def list_dashboard_widgets(
    is_active: bool = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List dashboard widgets"""
    try:
        query = db.query(DashboardWidget)
        
        if is_active is not None:
            query = query.filter(DashboardWidget.is_active == is_active)
        
        widgets = query.offset(skip).limit(limit).all()
        
        return [
            {
                "id": widget.id,
                "widget_name": widget.widget_name,
                "widget_type": widget.widget_type,
                "title": widget.title,
                "description": widget.description,
                "configuration": widget.configuration,
                "data_query": widget.data_query,
                "refresh_interval": widget.refresh_interval,
                "is_active": widget.is_active,
                "position_x": widget.position_x,
                "position_y": widget.position_y,
                "width": widget.width,
                "height": widget.height,
                "created_at": widget.created_at
            }
            for widget in widgets
        ]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/trends/overview")
async def get_trends_overview(days: int = 30):
    """Get overview of all trends"""
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Get data for different metrics
        customer_satisfaction_data = await tigerdata_client.get_time_series_data(
            "customer_satisfaction_calls", start_date, end_date
        )
        
        # Calculate overview metrics
        overview = {
            "period_days": days,
            "customer_satisfaction": {
                "data_points": len(customer_satisfaction_data),
                "trend": "stable"  # Would calculate actual trend
            },
            "recommendations": [
                "Monitor customer satisfaction trends weekly",
                "Set up alerts for significant changes",
                "Review competitor pricing monthly"
            ],
            "last_updated": datetime.now().isoformat()
        }
        
        return overview
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
