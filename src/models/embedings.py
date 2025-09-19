# src/models/embeddings.py
from sentence_transformers import SentenceTransformer
import numpy as np

class EmbeddingManager:
    def __init__(self):
        # Use a lightweight model for hackathon
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
    
    def create_embedding(self, text):
        """Create vector embedding for text"""
        embedding = self.model.encode([text])
        return embedding[0].tolist()
    
    def create_batch_embeddings(self, texts):
        """Create embeddings for multiple texts"""
        embeddings = self.model.encode(texts)
        return embeddings.tolist()
    
    def calculate_similarity(self, embedding1, embedding2):
        """Calculate cosine similarity between two embeddings"""
        emb1 = np.array(embedding1)
        emb2 = np.array(embedding2)
        return np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))

# Test the embedding system
def test_embeddings():
    em = EmbeddingManager()
    
    # Test with sample business situations
    situations = [
        "Customer complains about slow service during lunch rush",
        "Competitor lowered prices, losing customers",
        "Many negative reviews about food quality"
    ]
    
    embeddings = em.create_batch_embeddings(situations)
    print(f"✅ Created {len(embeddings)} embeddings, each with {len(embeddings[0])} dimensions")
    
    return em

if __name__ == "__main__":
    test_embeddings()