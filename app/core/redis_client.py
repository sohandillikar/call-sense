"""
Redis client configuration for vector search and caching
"""
import redis
import json
import numpy as np
from typing import List, Dict, Any, Optional
from app.core.config import settings


class RedisClient:
    """Redis client for vector search and caching"""
    
    def __init__(self):
        self.redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
        self.vector_dimension = settings.VECTOR_DIMENSION
    
    async def store_vector(self, key: str, vector: List[float], metadata: Dict[str, Any]) -> bool:
        """Store a vector with metadata in Redis"""
        try:
            # Store vector as JSON
            vector_data = {
                "vector": vector,
                "metadata": metadata
            }
            self.redis_client.set(key, json.dumps(vector_data))
            return True
        except Exception as e:
            print(f"Error storing vector: {e}")
            return False
    
    async def get_vector(self, key: str) -> Optional[Dict[str, Any]]:
        """Retrieve a vector with metadata from Redis"""
        try:
            data = self.redis_client.get(key)
            if data:
                return json.loads(data)
            return None
        except Exception as e:
            print(f"Error retrieving vector: {e}")
            return None
    
    async def search_similar_vectors(self, query_vector: List[float], limit: int = 10) -> List[Dict[str, Any]]:
        """Search for similar vectors using cosine similarity"""
        try:
            # Get all vector keys
            keys = self.redis_client.keys("vector:*")
            results = []
            
            for key in keys:
                vector_data = await self.get_vector(key)
                if vector_data and "vector" in vector_data:
                    # Calculate cosine similarity
                    similarity = self._cosine_similarity(query_vector, vector_data["vector"])
                    
                    if similarity >= settings.SIMILARITY_THRESHOLD:
                        results.append({
                            "key": key,
                            "similarity": similarity,
                            "metadata": vector_data.get("metadata", {})
                        })
            
            # Sort by similarity and return top results
            results.sort(key=lambda x: x["similarity"], reverse=True)
            return results[:limit]
            
        except Exception as e:
            print(f"Error searching similar vectors: {e}")
            return []
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors"""
        try:
            vec1_np = np.array(vec1)
            vec2_np = np.array(vec2)
            
            dot_product = np.dot(vec1_np, vec2_np)
            norm1 = np.linalg.norm(vec1_np)
            norm2 = np.linalg.norm(vec2_np)
            
            if norm1 == 0 or norm2 == 0:
                return 0.0
            
            return dot_product / (norm1 * norm2)
        except Exception:
            return 0.0
    
    async def cache_data(self, key: str, data: Any, expire_seconds: int = 3600) -> bool:
        """Cache data in Redis with expiration"""
        try:
            self.redis_client.setex(key, expire_seconds, json.dumps(data))
            return True
        except Exception as e:
            print(f"Error caching data: {e}")
            return False
    
    async def get_cached_data(self, key: str) -> Optional[Any]:
        """Retrieve cached data from Redis"""
        try:
            data = self.redis_client.get(key)
            if data:
                return json.loads(data)
            return None
        except Exception as e:
            print(f"Error retrieving cached data: {e}")
            return None


# Global Redis client instance
redis_client = RedisClient()
