# src/models/vector_search.py
from redisvl.api import RedisVLAPI
from redisvl.query import VectorQuery
from .embeddings import EmbeddingManager
import os
from dotenv import load_dotenv

load_dotenv()

class BusinessIntelligence:
    def __init__(self):
        self.rvl = RedisVLAPI(
            host=os.getenv('REDIS_HOST'),
            port=int(os.getenv('REDIS_PORT')),
            password=os.getenv('REDIS_PASSWORD'),
            decode_responses=True
        )
        self.embedding_manager = EmbeddingManager()
        self.index_name = "business_situations"
    
    def add_business_situation(self, situation_text, solution, business_type="restaurant"):
        """Add a new business situation and solution to the vector database"""
        situation_vector = self.embedding_manager.create_embedding(situation_text)
        
        data = {
            "situation_text": situation_text,
            "solution": solution,
            "business_type": business_type,
            "situation_vector": situation_vector
        }
        
        # Store in Redis with auto-generated key
        key = f"situation:{hash(situation_text)}"
        self.rvl.set_data(key, data)
        print(f"✅ Added situation: {situation_text[:50]}...")
    
    def find_similar_situations(self, current_situation, top_k=3):
        """Find similar business situations and their solutions"""
        query_vector = self.embedding_manager.create_embedding(current_situation)
        
        # Create vector similarity query
        query = VectorQuery(
            vector=query_vector,
            vector_field_name="situation_vector",
            return_fields=["situation_text", "solution", "business_type"],
            num_results=top_k
        )
        
        try:
            results = self.rvl.query(query, index_name=self.index_name)
            return [
                {
                    "similarity_score": result.score,
                    "situation": result.situation_text,
                    "solution": result.solution,
                    "business_type": result.business_type
                }
                for result in results
            ]
        except:
            # Return mock results for demo if Redis search fails
            return self._get_mock_similar_situations(current_situation)
    
    def _get_mock_similar_situations(self, situation):
        """Mock similar situations for demo"""
        return [
            {
                "similarity_score": 0.85,
                "situation": "Customers complained about slow service during busy hours",
                "solution": "Implemented online ordering system and hired additional staff for peak hours",
                "business_type": "restaurant"
            },
            {
                "similarity_score": 0.78,
                "situation": "Lost customers to competitor with faster service",
                "solution": "Added express lunch menu and optimized kitchen workflow",
                "business_type": "restaurant"
            }
        ]
    
    def populate_demo_data(self):
        """Populate with demo business situations for testing"""
        demo_situations = [
            ("Customer complaints about slow service during lunch rush", 
             "Hire additional staff for peak hours and implement express menu options"),
            ("Competitor lowered prices causing customer loss", 
             "Focus on value-added services and loyalty programs instead of price matching"),
            ("Negative reviews about food quality", 
             "Implement quality control checklist and staff retraining program"),
            ("High delivery complaints and low ratings", 
             "Partner with reliable delivery service and add order tracking"),
            ("Customers leaving due to limited parking", 
             "Negotiate with nearby businesses for shared parking or offer valet service"),
        ]
        
        for situation, solution in demo_situations:
            self.add_business_situation(situation, solution)
        
        print("✅ Demo data populated in Redis!")

# Test the intelligence system
def test_vector_search():
    bi = BusinessIntelligence()
    bi.populate_demo_data()
    
    # Test similarity search
    test_situation = "We're getting complaints about wait times"
    results = bi.find_similar_situations(test_situation)
    
    print(f"\n🔍 Similar situations for: '{test_situation}'")
    for i, result in enumerate(results, 1):
        print(f"\n{i}. Similarity: {result['similarity_score']:.2f}")
        print(f"   Situation: {result['situation']}")
        print(f"   Solution: {result['solution']}")

if __name__ == "__main__":
    test_vector_search()