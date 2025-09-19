"""
Vector search service for finding similar past issues and solutions
"""
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any, Optional, Tuple
from app.core.redis_client import redis_client
from app.core.config import settings
import json
import asyncio


class VectorSearchService:
    """Service for vector-based similarity search"""
    
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')  # Lightweight model for embeddings
        self.vector_dimension = settings.VECTOR_DIMENSION
    
    async def create_embedding(self, text: str) -> List[float]:
        """Create embedding vector for text"""
        try:
            # Clean and preprocess text
            cleaned_text = self._preprocess_text(text)
            
            # Generate embedding
            embedding = self.model.encode(cleaned_text)
            
            # Convert to list and ensure correct dimension
            embedding_list = embedding.tolist()
            
            return embedding_list
            
        except Exception as e:
            print(f"Error creating embedding: {e}")
            return []
    
    def _preprocess_text(self, text: str) -> str:
        """Preprocess text for embedding generation"""
        if not text:
            return ""
        
        # Basic text cleaning
        text = text.strip()
        text = text.replace('\n', ' ').replace('\r', ' ')
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text
    
    async def store_issue_solution(self, issue_text: str, solution_text: str, 
                                 metadata: Dict[str, Any]) -> str:
        """Store an issue-solution pair with vector embeddings"""
        try:
            # Create combined text for embedding
            combined_text = f"Issue: {issue_text} Solution: {solution_text}"
            
            # Generate embedding
            embedding = await self.create_embedding(combined_text)
            
            if not embedding:
                return ""
            
            # Create unique key
            import uuid
            key = f"issue_solution:{uuid.uuid4()}"
            
            # Prepare metadata
            vector_metadata = {
                "issue_text": issue_text,
                "solution_text": solution_text,
                "type": "issue_solution",
                "created_at": metadata.get("created_at"),
                "category": metadata.get("category", "general"),
                "tags": metadata.get("tags", []),
                **metadata
            }
            
            # Store in Redis
            success = await redis_client.store_vector(key, embedding, vector_metadata)
            
            if success:
                return key
            else:
                return ""
                
        except Exception as e:
            print(f"Error storing issue-solution: {e}")
            return ""
    
    async def store_call_insight(self, call_transcription: str, insights: Dict[str, Any],
                               metadata: Dict[str, Any]) -> str:
        """Store call insights with vector embeddings"""
        try:
            # Create text for embedding
            insight_text = f"Call: {call_transcription} Insights: {json.dumps(insights)}"
            
            # Generate embedding
            embedding = await self.create_embedding(insight_text)
            
            if not embedding:
                return ""
            
            # Create unique key
            import uuid
            key = f"call_insight:{uuid.uuid4()}"
            
            # Prepare metadata
            vector_metadata = {
                "call_transcription": call_transcription,
                "insights": insights,
                "type": "call_insight",
                "created_at": metadata.get("created_at"),
                "customer_id": metadata.get("customer_id"),
                "call_type": metadata.get("call_type"),
                **metadata
            }
            
            # Store in Redis
            success = await redis_client.store_vector(key, embedding, vector_metadata)
            
            if success:
                return key
            else:
                return ""
                
        except Exception as e:
            print(f"Error storing call insight: {e}")
            return ""
    
    async def store_review_insight(self, review_text: str, analysis: Dict[str, Any],
                                 metadata: Dict[str, Any]) -> str:
        """Store review insights with vector embeddings"""
        try:
            # Create text for embedding
            insight_text = f"Review: {review_text} Analysis: {json.dumps(analysis)}"
            
            # Generate embedding
            embedding = await self.create_embedding(insight_text)
            
            if not embedding:
                return ""
            
            # Create unique key
            import uuid
            key = f"review_insight:{uuid.uuid4()}"
            
            # Prepare metadata
            vector_metadata = {
                "review_text": review_text,
                "analysis": analysis,
                "type": "review_insight",
                "created_at": metadata.get("created_at"),
                "platform": metadata.get("platform"),
                "rating": metadata.get("rating"),
                **metadata
            }
            
            # Store in Redis
            success = await redis_client.store_vector(key, embedding, vector_metadata)
            
            if success:
                return key
            else:
                return ""
                
        except Exception as e:
            print(f"Error storing review insight: {e}")
            return ""
    
    async def find_similar_issues(self, query_text: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Find similar past issues and solutions"""
        try:
            # Create embedding for query
            query_embedding = await self.create_embedding(query_text)
            
            if not query_embedding:
                return []
            
            # Search for similar vectors
            similar_vectors = await redis_client.search_similar_vectors(query_embedding, limit * 2)
            
            # Filter for issue-solution pairs
            issue_solutions = []
            for result in similar_vectors:
                metadata = result.get("metadata", {})
                if metadata.get("type") == "issue_solution":
                    issue_solutions.append({
                        "similarity_score": result["similarity"],
                        "issue_text": metadata.get("issue_text", ""),
                        "solution_text": metadata.get("solution_text", ""),
                        "category": metadata.get("category", "general"),
                        "tags": metadata.get("tags", []),
                        "created_at": metadata.get("created_at"),
                        "key": result["key"]
                    })
            
            return issue_solutions[:limit]
            
        except Exception as e:
            print(f"Error finding similar issues: {e}")
            return []
    
    async def find_similar_calls(self, query_text: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Find similar past calls and insights"""
        try:
            # Create embedding for query
            query_embedding = await self.create_embedding(query_text)
            
            if not query_embedding:
                return []
            
            # Search for similar vectors
            similar_vectors = await redis_client.search_similar_vectors(query_embedding, limit * 2)
            
            # Filter for call insights
            call_insights = []
            for result in similar_vectors:
                metadata = result.get("metadata", {})
                if metadata.get("type") == "call_insight":
                    call_insights.append({
                        "similarity_score": result["similarity"],
                        "call_transcription": metadata.get("call_transcription", ""),
                        "insights": metadata.get("insights", {}),
                        "customer_id": metadata.get("customer_id"),
                        "call_type": metadata.get("call_type"),
                        "created_at": metadata.get("created_at"),
                        "key": result["key"]
                    })
            
            return call_insights[:limit]
            
        except Exception as e:
            print(f"Error finding similar calls: {e}")
            return []
    
    async def find_similar_reviews(self, query_text: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Find similar past reviews and analysis"""
        try:
            # Create embedding for query
            query_embedding = await self.create_embedding(query_text)
            
            if not query_embedding:
                return []
            
            # Search for similar vectors
            similar_vectors = await redis_client.search_similar_vectors(query_embedding, limit * 2)
            
            # Filter for review insights
            review_insights = []
            for result in similar_vectors:
                metadata = result.get("metadata", {})
                if metadata.get("type") == "review_insight":
                    review_insights.append({
                        "similarity_score": result["similarity"],
                        "review_text": metadata.get("review_text", ""),
                        "analysis": metadata.get("analysis", {}),
                        "platform": metadata.get("platform"),
                        "rating": metadata.get("rating"),
                        "created_at": metadata.get("created_at"),
                        "key": result["key"]
                    })
            
            return review_insights[:limit]
            
        except Exception as e:
            print(f"Error finding similar reviews: {e}")
            return []
    
    async def get_similarity_analysis(self, query_text: str) -> Dict[str, Any]:
        """Get comprehensive similarity analysis across all data types"""
        try:
            # Find similar items across all categories
            similar_issues = await self.find_similar_issues(query_text, 3)
            similar_calls = await self.find_similar_calls(query_text, 3)
            similar_reviews = await self.find_similar_reviews(query_text, 3)
            
            # Calculate overall similarity score
            all_similarities = []
            all_similarities.extend([item["similarity_score"] for item in similar_issues])
            all_similarities.extend([item["similarity_score"] for item in similar_calls])
            all_similarities.extend([item["similarity_score"] for item in similar_reviews])
            
            avg_similarity = np.mean(all_similarities) if all_similarities else 0.0
            max_similarity = max(all_similarities) if all_similarities else 0.0
            
            return {
                "query_text": query_text,
                "average_similarity": avg_similarity,
                "max_similarity": max_similarity,
                "total_matches": len(all_similarities),
                "similar_issues": similar_issues,
                "similar_calls": similar_calls,
                "similar_reviews": similar_reviews,
                "analysis_timestamp": asyncio.get_event_loop().time()
            }
            
        except Exception as e:
            print(f"Error in similarity analysis: {e}")
            return {
                "query_text": query_text,
                "error": str(e),
                "similar_issues": [],
                "similar_calls": [],
                "similar_reviews": []
            }


# Global service instance
vector_search_service = VectorSearchService()
