"""
Bright Data MCP client for competitor and company review monitoring
"""
import httpx
import asyncio
from typing import Dict, Any, Optional, List
from app.core.config import settings
import json
from datetime import datetime, timedelta


class BrightDataClient:
    """Client for interacting with Bright Data MCP API"""
    
    def __init__(self):
        self.api_key = settings.BRIGHT_DATA_API_KEY
        self.base_url = "https://api.brightdata.com"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def scrape_google_reviews(self, business_name: str, location: str = "") -> List[Dict[str, Any]]:
        """Scrape Google reviews for a business"""
        try:
            async with httpx.AsyncClient() as client:
                # Construct search query
                search_query = f"{business_name} {location}".strip()
                
                payload = {
                    "query": search_query,
                    "search_type": "google_reviews",
                    "max_results": 50,
                    "include_ratings": True,
                    "include_review_text": True,
                    "include_reviewer_info": True
                }
                
                response = await client.post(
                    f"{self.base_url}/scrape",
                    headers=self.headers,
                    json=payload,
                    timeout=120.0
                )
                response.raise_for_status()
                
                result = response.json()
                return self._parse_google_reviews(result)
                
        except httpx.HTTPError as e:
            print(f"Bright Data API error: {e}")
            return []
        except Exception as e:
            print(f"Unexpected error scraping Google reviews: {e}")
            return []
    
    async def scrape_yelp_reviews(self, business_name: str, location: str = "") -> List[Dict[str, Any]]:
        """Scrape Yelp reviews for a business"""
        try:
            async with httpx.AsyncClient() as client:
                search_query = f"{business_name} {location}".strip()
                
                payload = {
                    "query": search_query,
                    "search_type": "yelp_reviews",
                    "max_results": 50,
                    "include_ratings": True,
                    "include_review_text": True,
                    "include_reviewer_info": True
                }
                
                response = await client.post(
                    f"{self.base_url}/scrape",
                    headers=self.headers,
                    json=payload,
                    timeout=120.0
                )
                response.raise_for_status()
                
                result = response.json()
                return self._parse_yelp_reviews(result)
                
        except httpx.HTTPError as e:
            print(f"Bright Data API error: {e}")
            return []
        except Exception as e:
            print(f"Unexpected error scraping Yelp reviews: {e}")
            return []
    
    async def scrape_competitor_pricing(self, competitor_name: str, product_category: str = "") -> List[Dict[str, Any]]:
        """Scrape competitor pricing information"""
        try:
            async with httpx.AsyncClient() as client:
                search_query = f"{competitor_name} {product_category} price".strip()
                
                payload = {
                    "query": search_query,
                    "search_type": "ecommerce_pricing",
                    "max_results": 100,
                    "include_product_info": True,
                    "include_pricing": True,
                    "include_availability": True
                }
                
                response = await client.post(
                    f"{self.base_url}/scrape",
                    headers=self.headers,
                    json=payload,
                    timeout=120.0
                )
                response.raise_for_status()
                
                result = response.json()
                return self._parse_pricing_data(result)
                
        except httpx.HTTPError as e:
            print(f"Bright Data API error: {e}")
            return []
        except Exception as e:
            print(f"Unexpected error scraping pricing: {e}")
            return []
    
    async def scrape_competitor_website(self, competitor_url: str) -> Dict[str, Any]:
        """Scrape competitor website for general information"""
        try:
            async with httpx.AsyncClient() as client:
                payload = {
                    "url": competitor_url,
                    "extract_type": "full_page",
                    "include_metadata": True,
                    "include_links": True,
                    "include_images": False
                }
                
                response = await client.post(
                    f"{self.base_url}/scrape",
                    headers=self.headers,
                    json=payload,
                    timeout=60.0
                )
                response.raise_for_status()
                
                result = response.json()
                return self._parse_website_data(result)
                
        except httpx.HTTPError as e:
            print(f"Bright Data API error: {e}")
            return {}
        except Exception as e:
            print(f"Unexpected error scraping website: {e}")
            return {}
    
    def _parse_google_reviews(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Parse Google reviews data from Bright Data response"""
        reviews = []
        
        if "results" in data:
            for item in data["results"]:
                review = {
                    "platform": "google",
                    "reviewer_name": item.get("reviewer_name", ""),
                    "rating": float(item.get("rating", 0)),
                    "review_text": item.get("review_text", ""),
                    "review_date": item.get("review_date", ""),
                    "is_verified": item.get("is_verified", False),
                    "business_response": item.get("business_response", ""),
                    "helpful_votes": item.get("helpful_votes", 0),
                    "scraped_at": datetime.now().isoformat()
                }
                reviews.append(review)
        
        return reviews
    
    def _parse_yelp_reviews(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Parse Yelp reviews data from Bright Data response"""
        reviews = []
        
        if "results" in data:
            for item in data["results"]:
                review = {
                    "platform": "yelp",
                    "reviewer_name": item.get("reviewer_name", ""),
                    "rating": float(item.get("rating", 0)),
                    "review_text": item.get("review_text", ""),
                    "review_date": item.get("review_date", ""),
                    "is_verified": item.get("is_verified", False),
                    "business_response": item.get("business_response", ""),
                    "helpful_votes": item.get("helpful_votes", 0),
                    "scraped_at": datetime.now().isoformat()
                }
                reviews.append(review)
        
        return reviews
    
    def _parse_pricing_data(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Parse pricing data from Bright Data response"""
        pricing_data = []
        
        if "results" in data:
            for item in data["results"]:
                price_info = {
                    "competitor_name": item.get("competitor_name", ""),
                    "product_name": item.get("product_name", ""),
                    "product_category": item.get("product_category", ""),
                    "price": float(item.get("price", 0)),
                    "currency": item.get("currency", "USD"),
                    "availability": item.get("availability", "unknown"),
                    "product_url": item.get("product_url", ""),
                    "scraped_at": datetime.now().isoformat()
                }
                pricing_data.append(price_info)
        
        return pricing_data
    
    def _parse_website_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse website data from Bright Data response"""
        return {
            "url": data.get("url", ""),
            "title": data.get("title", ""),
            "description": data.get("description", ""),
            "content": data.get("content", ""),
            "links": data.get("links", []),
            "metadata": data.get("metadata", {}),
            "scraped_at": datetime.now().isoformat()
        }


class ReviewAnalysisService:
    """Service for analyzing reviews and generating insights"""
    
    def __init__(self):
        self.bright_data_client = BrightDataClient()
    
    async def analyze_review_sentiment(self, review_text: str) -> Dict[str, Any]:
        """Analyze sentiment of review text"""
        # Simple keyword-based sentiment analysis
        # In production, use a proper NLP model or API
        
        positive_keywords = [
            "excellent", "amazing", "wonderful", "fantastic", "great", "good",
            "love", "perfect", "outstanding", "brilliant", "superb", "terrific"
        ]
        
        negative_keywords = [
            "terrible", "awful", "horrible", "disappointing", "bad", "poor",
            "hate", "worst", "disgusting", "pathetic", "useless", "waste"
        ]
        
        text_lower = review_text.lower()
        
        positive_count = sum(1 for word in positive_keywords if word in text_lower)
        negative_count = sum(1 for word in negative_keywords if word in text_lower)
        
        total_sentiment_words = positive_count + negative_count
        
        if total_sentiment_words == 0:
            sentiment_score = 0.0
            sentiment_label = "neutral"
        else:
            sentiment_score = (positive_count - negative_count) / total_sentiment_words
            if sentiment_score > 0.1:
                sentiment_label = "positive"
            elif sentiment_score < -0.1:
                sentiment_label = "negative"
            else:
                sentiment_label = "neutral"
        
        return {
            "sentiment_score": sentiment_score,
            "sentiment_label": sentiment_label,
            "positive_indicators": positive_count,
            "negative_indicators": negative_count
        }
    
    async def extract_review_themes(self, review_text: str) -> List[str]:
        """Extract key themes from review text"""
        themes = {
            "customer_service": ["service", "staff", "employee", "helpful", "friendly", "rude"],
            "product_quality": ["quality", "product", "durable", "broken", "defective"],
            "pricing": ["price", "expensive", "cheap", "value", "cost", "affordable"],
            "delivery": ["delivery", "shipping", "fast", "slow", "late", "on time"],
            "website": ["website", "online", "easy", "difficult", "navigation"],
            "return_policy": ["return", "refund", "exchange", "policy"]
        }
        
        text_lower = review_text.lower()
        found_themes = []
        
        for theme, keywords in themes.items():
            if any(keyword in text_lower for keyword in keywords):
                found_themes.append(theme)
        
        return found_themes
    
    async def generate_competitive_insights(self, company_reviews: List[Dict[str, Any]], 
                                          competitor_reviews: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate competitive insights from review analysis"""
        # Analyze company reviews
        company_avg_rating = sum(r.get("rating", 0) for r in company_reviews) / len(company_reviews) if company_reviews else 0
        company_sentiment_scores = [r.get("sentiment_score", 0) for r in company_reviews if "sentiment_score" in r]
        company_avg_sentiment = sum(company_sentiment_scores) / len(company_sentiment_scores) if company_sentiment_scores else 0
        
        # Analyze competitor reviews
        competitor_avg_rating = sum(r.get("rating", 0) for r in competitor_reviews) / len(competitor_reviews) if competitor_reviews else 0
        competitor_sentiment_scores = [r.get("sentiment_score", 0) for r in competitor_reviews if "sentiment_score" in r]
        competitor_avg_sentiment = sum(competitor_sentiment_scores) / len(competitor_sentiment_scores) if competitor_sentiment_scores else 0
        
        # Generate insights
        insights = {
            "company_performance": {
                "average_rating": company_avg_rating,
                "average_sentiment": company_avg_sentiment,
                "total_reviews": len(company_reviews)
            },
            "competitor_performance": {
                "average_rating": competitor_avg_rating,
                "average_sentiment": competitor_avg_sentiment,
                "total_reviews": len(competitor_reviews)
            },
            "competitive_position": self._determine_competitive_position(
                company_avg_rating, competitor_avg_rating,
                company_avg_sentiment, competitor_avg_sentiment
            ),
            "recommendations": self._generate_recommendations(
                company_avg_rating, competitor_avg_rating,
                company_avg_sentiment, competitor_avg_sentiment
            )
        }
        
        return insights
    
    def _determine_competitive_position(self, company_rating: float, competitor_rating: float,
                                      company_sentiment: float, competitor_sentiment: float) -> str:
        """Determine competitive position based on ratings and sentiment"""
        rating_diff = company_rating - competitor_rating
        sentiment_diff = company_sentiment - competitor_sentiment
        
        if rating_diff > 0.5 and sentiment_diff > 0.1:
            return "leading"
        elif rating_diff < -0.5 and sentiment_diff < -0.1:
            return "lagging"
        else:
            return "competitive"
    
    def _generate_recommendations(self, company_rating: float, competitor_rating: float,
                                company_sentiment: float, competitor_sentiment: float) -> List[str]:
        """Generate recommendations based on competitive analysis"""
        recommendations = []
        
        if company_rating < competitor_rating:
            recommendations.append("Focus on improving product/service quality to match competitor ratings")
        
        if company_sentiment < competitor_sentiment:
            recommendations.append("Investigate and address customer satisfaction issues")
        
        if company_rating > competitor_rating and company_sentiment > competitor_sentiment:
            recommendations.append("Leverage superior performance in marketing and customer acquisition")
        
        if not recommendations:
            recommendations.append("Maintain current performance and monitor competitor activities")
        
        return recommendations


# Global service instances
bright_data_client = BrightDataClient()
review_analysis_service = ReviewAnalysisService()
