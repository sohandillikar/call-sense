"""
Gladia API client for call transcription and analysis
"""
import httpx
import asyncio
from typing import Dict, Any, Optional, List
from app.core.config import settings


class GladiaClient:
    """Client for interacting with Gladia API"""
    
    def __init__(self):
        self.api_key = settings.GLADIA_API_KEY
        self.base_url = "https://api.gladia.io/v2"
        self.headers = {
            "x-gladia-key": self.api_key,
            "Content-Type": "application/json"
        }
    
    async def transcribe_audio(self, audio_url: str, language: str = "en") -> Dict[str, Any]:
        """Transcribe audio file from URL"""
        try:
            async with httpx.AsyncClient() as client:
                payload = {
                    "audio_url": audio_url,
                    "language": language,
                    "transcription": {
                        "include_timestamps": True,
                        "include_speakers": True
                    }
                }
                
                response = await client.post(
                    f"{self.base_url}/transcription",
                    headers=self.headers,
                    json=payload,
                    timeout=60.0
                )
                response.raise_for_status()
                return response.json()
                
        except httpx.HTTPError as e:
            print(f"Gladia API error: {e}")
            return {"error": str(e)}
        except Exception as e:
            print(f"Unexpected error: {e}")
            return {"error": str(e)}
    
    async def transcribe_file(self, file_path: str, language: str = "en") -> Dict[str, Any]:
        """Transcribe audio file from local path"""
        try:
            async with httpx.AsyncClient() as client:
                with open(file_path, "rb") as audio_file:
                    files = {"audio": audio_file}
                    data = {
                        "language": language,
                        "transcription": {
                            "include_timestamps": True,
                            "include_speakers": True
                        }
                    }
                    
                    response = await client.post(
                        f"{self.base_url}/transcription",
                        headers={"x-gladia-key": self.api_key},
                        files=files,
                        data=data,
                        timeout=60.0
                    )
                    response.raise_for_status()
                    return response.json()
                    
        except httpx.HTTPError as e:
            print(f"Gladia API error: {e}")
            return {"error": str(e)}
        except Exception as e:
            print(f"Unexpected error: {e}")
            return {"error": str(e)}
    
    async def get_transcription_status(self, transcription_id: str) -> Dict[str, Any]:
        """Get the status of a transcription job"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/transcription/{transcription_id}",
                    headers=self.headers,
                    timeout=30.0
                )
                response.raise_for_status()
                return response.json()
                
        except httpx.HTTPError as e:
            print(f"Gladia API error: {e}")
            return {"error": str(e)}
        except Exception as e:
            print(f"Unexpected error: {e}")
            return {"error": str(e)}
    
    def extract_transcription_text(self, transcription_result: Dict[str, Any]) -> str:
        """Extract plain text from Gladia transcription result"""
        if "error" in transcription_result:
            return ""
        
        transcription = transcription_result.get("transcription", {})
        if not transcription:
            return ""
        
        # Extract text from segments
        segments = transcription.get("full_transcript", [])
        if not segments:
            return ""
        
        # Combine all segments into a single text
        text_parts = []
        for segment in segments:
            if isinstance(segment, dict) and "text" in segment:
                text_parts.append(segment["text"])
            elif isinstance(segment, str):
                text_parts.append(segment)
        
        return " ".join(text_parts)
    
    def extract_speakers(self, transcription_result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract speaker information from transcription"""
        if "error" in transcription_result:
            return []
        
        transcription = transcription_result.get("transcription", {})
        speakers = transcription.get("speakers", [])
        
        return speakers if isinstance(speakers, list) else []


class CallAnalysisService:
    """Service for analyzing call transcriptions and generating insights"""
    
    def __init__(self):
        self.gladia_client = GladiaClient()
    
    async def analyze_call_sentiment(self, transcription_text: str) -> Dict[str, Any]:
        """Analyze sentiment of call transcription"""
        # This would typically use an AI service like OpenAI or a sentiment analysis model
        # For now, we'll implement a simple keyword-based approach
        
        positive_keywords = [
            "good", "great", "excellent", "amazing", "wonderful", "fantastic",
            "love", "like", "happy", "satisfied", "pleased", "thank you"
        ]
        
        negative_keywords = [
            "bad", "terrible", "awful", "hate", "disappointed", "angry",
            "frustrated", "upset", "problem", "issue", "complaint", "refund"
        ]
        
        text_lower = transcription_text.lower()
        
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
    
    async def extract_key_topics(self, transcription_text: str) -> List[str]:
        """Extract key topics from call transcription"""
        # Simple keyword extraction - in production, use NLP models
        common_topics = {
            "billing": ["bill", "payment", "charge", "cost", "price", "invoice"],
            "support": ["help", "support", "assistance", "problem", "issue"],
            "product": ["product", "service", "feature", "functionality"],
            "account": ["account", "profile", "settings", "login", "password"],
            "shipping": ["shipping", "delivery", "order", "tracking"],
            "refund": ["refund", "return", "cancel", "exchange"]
        }
        
        text_lower = transcription_text.lower()
        found_topics = []
        
        for topic, keywords in common_topics.items():
            if any(keyword in text_lower for keyword in keywords):
                found_topics.append(topic)
        
        return found_topics
    
    async def generate_action_items(self, transcription_text: str, sentiment_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate action items from call transcription"""
        action_items = []
        
        # Generate action items based on sentiment and content
        if sentiment_analysis["sentiment_label"] == "negative":
            action_items.append({
                "action": "Follow up with customer",
                "priority": "high",
                "description": "Customer expressed negative sentiment - immediate follow-up required"
            })
        
        if "refund" in transcription_text.lower():
            action_items.append({
                "action": "Process refund request",
                "priority": "high",
                "description": "Customer mentioned refund - review and process if valid"
            })
        
        if "billing" in transcription_text.lower():
            action_items.append({
                "action": "Review billing inquiry",
                "priority": "medium",
                "description": "Customer has billing-related questions"
            })
        
        return action_items
    
    async def calculate_priority_score(self, sentiment_analysis: Dict[str, Any], action_items: List[Dict[str, Any]]) -> float:
        """Calculate priority score for the call (0-1)"""
        base_score = 0.5
        
        # Adjust based on sentiment
        if sentiment_analysis["sentiment_label"] == "negative":
            base_score += 0.3
        elif sentiment_analysis["sentiment_label"] == "positive":
            base_score -= 0.1
        
        # Adjust based on action items
        high_priority_items = sum(1 for item in action_items if item.get("priority") == "high")
        base_score += high_priority_items * 0.1
        
        return min(1.0, max(0.0, base_score))


# Global service instances
gladia_client = GladiaClient()
call_analysis_service = CallAnalysisService()
