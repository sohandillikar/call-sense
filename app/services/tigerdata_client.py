"""
TigerData client for time-series data storage and analysis
"""
import httpx
import asyncio
from typing import Dict, Any, Optional, List, Tuple
from app.core.config import settings
import json
from datetime import datetime, timedelta
import pandas as pd
import numpy as np


class TigerDataClient:
    """Client for interacting with TigerData API"""
    
    def __init__(self):
        self.api_key = settings.TIGERDATA_API_KEY
        self.base_url = "https://api.tigerdata.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def store_time_series_data(self, metric_name: str, data_points: List[Dict[str, Any]]) -> bool:
        """Store time-series data points"""
        try:
            async with httpx.AsyncClient() as client:
                payload = {
                    "metric_name": metric_name,
                    "data_points": data_points,
                    "timestamp": datetime.now().isoformat()
                }
                
                response = await client.post(
                    f"{self.base_url}/timeseries",
                    headers=self.headers,
                    json=payload,
                    timeout=30.0
                )
                response.raise_for_status()
                return True
                
        except httpx.HTTPError as e:
            print(f"TigerData API error: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error storing time series data: {e}")
            return False
    
    async def get_time_series_data(self, metric_name: str, start_date: datetime, 
                                 end_date: datetime) -> List[Dict[str, Any]]:
        """Retrieve time-series data for a specific metric and date range"""
        try:
            async with httpx.AsyncClient() as client:
                params = {
                    "metric_name": metric_name,
                    "start_date": start_date.isoformat(),
                    "end_date": end_date.isoformat()
                }
                
                response = await client.get(
                    f"{self.base_url}/timeseries",
                    headers=self.headers,
                    params=params,
                    timeout=30.0
                )
                response.raise_for_status()
                
                result = response.json()
                return result.get("data_points", [])
                
        except httpx.HTTPError as e:
            print(f"TigerData API error: {e}")
            return []
        except Exception as e:
            print(f"Unexpected error retrieving time series data: {e}")
            return []
    
    async def get_aggregated_data(self, metric_name: str, start_date: datetime, 
                                end_date: datetime, aggregation: str = "daily") -> List[Dict[str, Any]]:
        """Get aggregated time-series data"""
        try:
            async with httpx.AsyncClient() as client:
                params = {
                    "metric_name": metric_name,
                    "start_date": start_date.isoformat(),
                    "end_date": end_date.isoformat(),
                    "aggregation": aggregation
                }
                
                response = await client.get(
                    f"{self.base_url}/timeseries/aggregated",
                    headers=self.headers,
                    params=params,
                    timeout=30.0
                )
                response.raise_for_status()
                
                result = response.json()
                return result.get("aggregated_data", [])
                
        except httpx.HTTPError as e:
            print(f"TigerData API error: {e}")
            return []
        except Exception as e:
            print(f"Unexpected error retrieving aggregated data: {e}")
            return []
    
    async def create_dashboard(self, dashboard_config: Dict[str, Any]) -> str:
        """Create a new dashboard"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/dashboards",
                    headers=self.headers,
                    json=dashboard_config,
                    timeout=30.0
                )
                response.raise_for_status()
                
                result = response.json()
                return result.get("dashboard_id", "")
                
        except httpx.HTTPError as e:
            print(f"TigerData API error: {e}")
            return ""
        except Exception as e:
            print(f"Unexpected error creating dashboard: {e}")
            return ""
    
    async def get_dashboard_data(self, dashboard_id: str) -> Dict[str, Any]:
        """Get dashboard data and visualizations"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/dashboards/{dashboard_id}",
                    headers=self.headers,
                    timeout=30.0
                )
                response.raise_for_status()
                
                return response.json()
                
        except httpx.HTTPError as e:
            print(f"TigerData API error: {e}")
            return {}
        except Exception as e:
            print(f"Unexpected error retrieving dashboard: {e}")
            return {}


class TimeSeriesAnalysisService:
    """Service for analyzing time-series data and generating insights"""
    
    def __init__(self):
        self.tigerdata_client = TigerDataClient()
    
    async def store_competitor_pricing_trends(self, competitor_name: str, 
                                            pricing_data: List[Dict[str, Any]]) -> bool:
        """Store competitor pricing trends as time-series data"""
        try:
            metric_name = f"competitor_pricing_{competitor_name.lower().replace(' ', '_')}"
            
            # Convert pricing data to time-series format
            data_points = []
            for item in pricing_data:
                data_point = {
                    "timestamp": item.get("scraped_at", datetime.now().isoformat()),
                    "value": item.get("price", 0),
                    "metadata": {
                        "product_name": item.get("product_name", ""),
                        "product_category": item.get("product_category", ""),
                        "availability": item.get("availability", ""),
                        "currency": item.get("currency", "USD")
                    }
                }
                data_points.append(data_point)
            
            return await self.tigerdata_client.store_time_series_data(metric_name, data_points)
            
        except Exception as e:
            print(f"Error storing competitor pricing trends: {e}")
            return False
    
    async def store_review_sentiment_trends(self, company_name: str, 
                                          review_data: List[Dict[str, Any]]) -> bool:
        """Store review sentiment trends as time-series data"""
        try:
            metric_name = f"review_sentiment_{company_name.lower().replace(' ', '_')}"
            
            # Convert review data to time-series format
            data_points = []
            for item in review_data:
                data_point = {
                    "timestamp": item.get("review_date", datetime.now().isoformat()),
                    "value": item.get("sentiment_score", 0),
                    "metadata": {
                        "rating": item.get("rating", 0),
                        "platform": item.get("platform", ""),
                        "review_text": item.get("review_text", "")[:100]  # Truncate for storage
                    }
                }
                data_points.append(data_point)
            
            return await self.tigerdata_client.store_time_series_data(metric_name, data_points)
            
        except Exception as e:
            print(f"Error storing review sentiment trends: {e}")
            return False
    
    async def store_customer_satisfaction_trends(self, call_data: List[Dict[str, Any]]) -> bool:
        """Store customer satisfaction trends from call data"""
        try:
            metric_name = "customer_satisfaction_calls"
            
            # Convert call data to time-series format
            data_points = []
            for item in call_data:
                data_point = {
                    "timestamp": item.get("created_at", datetime.now().isoformat()),
                    "value": item.get("sentiment_score", 0),
                    "metadata": {
                        "call_type": item.get("call_type", ""),
                        "duration": item.get("duration_seconds", 0),
                        "priority_score": item.get("priority_score", 0)
                    }
                }
                data_points.append(data_point)
            
            return await self.tigerdata_client.store_time_series_data(metric_name, data_points)
            
        except Exception as e:
            print(f"Error storing customer satisfaction trends: {e}")
            return False
    
    async def analyze_pricing_trends(self, competitor_name: str, days: int = 30) -> Dict[str, Any]:
        """Analyze competitor pricing trends over time"""
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            metric_name = f"competitor_pricing_{competitor_name.lower().replace(' ', '_')}"
            data_points = await self.tigerdata_client.get_time_series_data(
                metric_name, start_date, end_date
            )
            
            if not data_points:
                return {"error": "No data available"}
            
            # Convert to DataFrame for analysis
            df = pd.DataFrame(data_points)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df['value'] = pd.to_numeric(df['value'])
            
            # Calculate trends
            trend_analysis = {
                "competitor_name": competitor_name,
                "period_days": days,
                "total_data_points": len(data_points),
                "average_price": df['value'].mean(),
                "price_range": {
                    "min": df['value'].min(),
                    "max": df['value'].max()
                },
                "trend_direction": self._calculate_trend_direction(df['value']),
                "volatility": df['value'].std(),
                "recent_changes": self._analyze_recent_changes(df),
                "recommendations": self._generate_pricing_recommendations(df)
            }
            
            return trend_analysis
            
        except Exception as e:
            print(f"Error analyzing pricing trends: {e}")
            return {"error": str(e)}
    
    async def analyze_sentiment_trends(self, company_name: str, days: int = 30) -> Dict[str, Any]:
        """Analyze sentiment trends over time"""
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            metric_name = f"review_sentiment_{company_name.lower().replace(' ', '_')}"
            data_points = await self.tigerdata_client.get_time_series_data(
                metric_name, start_date, end_date
            )
            
            if not data_points:
                return {"error": "No data available"}
            
            # Convert to DataFrame for analysis
            df = pd.DataFrame(data_points)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df['value'] = pd.to_numeric(df['value'])
            
            # Calculate sentiment trends
            sentiment_analysis = {
                "company_name": company_name,
                "period_days": days,
                "total_data_points": len(data_points),
                "average_sentiment": df['value'].mean(),
                "sentiment_range": {
                    "min": df['value'].min(),
                    "max": df['value'].max()
                },
                "trend_direction": self._calculate_trend_direction(df['value']),
                "sentiment_stability": 1 - df['value'].std(),  # Higher = more stable
                "recent_sentiment": df['value'].tail(7).mean(),  # Last 7 days
                "recommendations": self._generate_sentiment_recommendations(df)
            }
            
            return sentiment_analysis
            
        except Exception as e:
            print(f"Error analyzing sentiment trends: {e}")
            return {"error": str(e)}
    
    def _calculate_trend_direction(self, values: pd.Series) -> str:
        """Calculate trend direction from time series data"""
        if len(values) < 2:
            return "insufficient_data"
        
        # Simple linear trend calculation
        x = np.arange(len(values))
        slope = np.polyfit(x, values, 1)[0]
        
        if slope > 0.01:
            return "increasing"
        elif slope < -0.01:
            return "decreasing"
        else:
            return "stable"
    
    def _analyze_recent_changes(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze recent changes in the data"""
        if len(df) < 7:
            return {"error": "Insufficient data for recent analysis"}
        
        recent_data = df.tail(7)
        previous_data = df.tail(14).head(7)
        
        recent_avg = recent_data['value'].mean()
        previous_avg = previous_data['value'].mean()
        
        change_percentage = ((recent_avg - previous_avg) / previous_avg) * 100 if previous_avg != 0 else 0
        
        return {
            "recent_average": recent_avg,
            "previous_average": previous_avg,
            "change_percentage": change_percentage,
            "change_direction": "increase" if change_percentage > 0 else "decrease" if change_percentage < 0 else "stable"
        }
    
    def _generate_pricing_recommendations(self, df: pd.DataFrame) -> List[str]:
        """Generate pricing recommendations based on trend analysis"""
        recommendations = []
        
        trend = self._calculate_trend_direction(df['value'])
        volatility = df['value'].std()
        
        if trend == "increasing":
            recommendations.append("Competitor prices are trending upward - consider monitoring for pricing opportunities")
        elif trend == "decreasing":
            recommendations.append("Competitor prices are declining - assess competitive pressure")
        
        if volatility > df['value'].mean() * 0.1:  # High volatility
            recommendations.append("High price volatility detected - monitor for promotional activities")
        
        if len(recommendations) == 0:
            recommendations.append("Pricing appears stable - continue monitoring for changes")
        
        return recommendations
    
    def _generate_sentiment_recommendations(self, df: pd.DataFrame) -> List[str]:
        """Generate sentiment recommendations based on trend analysis"""
        recommendations = []
        
        trend = self._calculate_trend_direction(df['value'])
        recent_sentiment = df['value'].tail(7).mean()
        
        if trend == "decreasing":
            recommendations.append("Sentiment is declining - investigate recent customer feedback")
        elif trend == "increasing":
            recommendations.append("Sentiment is improving - leverage positive momentum")
        
        if recent_sentiment < -0.1:
            recommendations.append("Recent sentiment is negative - prioritize customer satisfaction initiatives")
        elif recent_sentiment > 0.1:
            recommendations.append("Recent sentiment is positive - consider amplifying positive feedback")
        
        if len(recommendations) == 0:
            recommendations.append("Sentiment is stable - continue monitoring customer feedback")
        
        return recommendations
    
    async def create_business_dashboard(self, company_name: str) -> str:
        """Create a comprehensive business dashboard"""
        try:
            dashboard_config = {
                "name": f"{company_name} Business Dashboard",
                "description": "Comprehensive business analytics dashboard",
                "widgets": [
                    {
                        "type": "line_chart",
                        "title": "Customer Satisfaction Trends",
                        "metric": "customer_satisfaction_calls",
                        "time_range": "30d"
                    },
                    {
                        "type": "line_chart",
                        "title": "Review Sentiment Trends",
                        "metric": f"review_sentiment_{company_name.lower().replace(' ', '_')}",
                        "time_range": "30d"
                    },
                    {
                        "type": "bar_chart",
                        "title": "Competitor Pricing Comparison",
                        "metrics": ["competitor_pricing_*"],
                        "time_range": "7d"
                    },
                    {
                        "type": "metric_card",
                        "title": "Average Customer Rating",
                        "metric": f"review_sentiment_{company_name.lower().replace(' ', '_')}",
                        "aggregation": "avg"
                    }
                ],
                "refresh_interval": 3600,  # 1 hour
                "is_public": False
            }
            
            return await self.tigerdata_client.create_dashboard(dashboard_config)
            
        except Exception as e:
            print(f"Error creating business dashboard: {e}")
            return ""


# Global service instances
tigerdata_client = TigerDataClient()
time_series_analysis_service = TimeSeriesAnalysisService()
