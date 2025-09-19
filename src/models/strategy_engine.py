# src/models/strategy_engine.py
from .vector_search import BusinessIntelligence
from ..api.bright_data_client import BrightDataClient
from ..data.database import get_recent_trends
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

class StrategyEngine:
    def __init__(self):
        self.business_intelligence = BusinessIntelligence()
        self.bright_data = BrightDataClient()
        self.business_name = os.getenv('TEST_BUSINESS_NAME', "Mario's Pizza Palace")
        self.business_type = os.getenv('TEST_BUSINESS_TYPE', "restaurant")
    
    def analyze_customer_issue(self, customer_issue, call_transcription=""):
        """Analyze customer issue and provide strategic recommendations"""
        print(f"🔍 Analyzing customer issue: {customer_issue}")
        
        # 1. Find similar past situations using Redis Vector Search
        similar_situations = self.business_intelligence.find_similar_situations(customer_issue)
        
        # 2. Get competitor intelligence
        competitor_data = self.bright_data.scrape_competitor_pricing(self.business_type)
        
        # 3. Analyze recent trends from TigerData
        recent_trends = self._get_recent_business_trends()
        
        # 4. Generate strategic recommendations
        recommendations = self._generate_recommendations(
            customer_issue, similar_situations, competitor_data, recent_trends
        )
        
        return {
            "customer_issue": customer_issue,
            "similar_situations": similar_situations,
            "competitor_analysis": competitor_data,
            "trends": recent_trends,
            "recommendations": recommendations,
            "priority_level": self._assess_priority(customer_issue)
        }
    
    def _generate_recommendations(self, issue, similar_situations, competitors, trends):
        """Generate strategic business recommendations"""
        recommendations = []
        
        # Based on similar situations
        if similar_situations:
            top_solution = similar_situations[0]['solution']
            recommendations.append({
                "type": "proven_solution",
                "action": top_solution,
                "confidence": similar_situations[0]['similarity_score'],
                "source": "Similar past situations"
            })
        
        # Based on competitor analysis
        if competitors:
            avg_competitor_price = sum(c['price'] for c in competitors) / len(competitors)
            recommendations.append({
                "type": "competitive_positioning",
                "action": f"Consider competitive pricing - market average is ${avg_competitor_price:.2f}",
                "confidence": 0.7,
                "source": "Competitor analysis"
            })
        
        # Based on issue type
        issue_lower = issue.lower()
        if 'slow' in issue_lower or 'wait' in issue_lower:
            recommendations.append({
                "type": "operational_improvement",
                "action": "Implement online ordering system to reduce wait times",
                "confidence": 0.8,
                "source": "Issue pattern analysis"
            })
        elif 'price' in issue_lower or 'expensive' in issue_lower:
            recommendations.append({
                "type": "pricing_strategy",
                "action": "Consider value meal options or loyalty program",
                "confidence": 0.75,
                "source": "Price sensitivity analysis"
            })
        
        return recommendations
    
    def _assess_priority(self, issue):
        """Assess the priority level of the issue"""
        high_priority_keywords = ['complaint', 'angry', 'cancel', 'refund', 'terrible']
        issue_lower = issue.lower()
        
        if any(keyword in issue_lower for keyword in high_priority_keywords):
            return "HIGH"
        elif any(word in issue_lower for word in ['slow', 'wait', 'problem']):
            return "MEDIUM"
        else:
            return "LOW"
    
    def _get_recent_business_trends(self):
        """Get recent trends from TigerData (mock for demo)"""
        # In real implementation, query TigerData for recent trends
        return {
            "customer_calls_trend": "20% increase in calls this week",
            "review_sentiment": "Average rating dropped from 4.2 to 3.8",
            "competitor_activity": "2 competitors lowered prices this month"
        }
    
    def get_business_dashboard(self):
        """Generate comprehensive business intelligence dashboard"""
        # Get recent competitor data
        competitor_data = self.bright_data.scrape_competitor_pricing(self.business_type)
        reviews = self.bright_data.scrape_reviews(self.business_name)
        
        # Calculate insights
        avg_competitor_price = sum(c['price'] for c in competitor_data) / len(competitor_data) if competitor_data else 0
        avg_rating = sum(r['rating'] for r in reviews) / len(reviews) if reviews else 0
        
        return {
            "business_name": self.business_name,
            "competitor_analysis": {
                "average_competitor_price": avg_competitor_price,
                "competitors_tracked": len(competitor_data),
                "price_position": "above_average" if avg_competitor_price > 20 else "competitive"
            },
            "reputation_analysis": {
                "average_rating": avg_rating,
                "total_reviews": len(reviews),
                "recent_reviews": reviews[:3]
            },
            "strategic_insights": [
                "Monitor competitor pricing weekly for market positioning",
                "Address service speed issues mentioned in recent reviews",
                "Consider loyalty program to improve customer retention"
            ]
        }

# Test the strategy engine
def test_strategy_engine():
    engine = StrategyEngine()
    
    # Test customer issue analysis
    test_issue = "Customer called complaining about 30-minute wait time for pizza"
    analysis = engine.analyze_customer_issue(test_issue)
    
    print("🎯 Strategic Analysis Results:")
    print(f"Issue: {analysis['customer_issue']}")
    print(f"Priority: {analysis['priority_level']}")
    print("\n📋 Recommendations:")
    for i, rec in enumerate(analysis['recommendations'], 1):
        print(f"{i}. {rec['action']} (Confidence: {rec['confidence']:.1%})")
    
    return engine

if __name__ == "__main__":
    test_strategy_engine()