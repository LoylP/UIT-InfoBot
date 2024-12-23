import os
import faiss
import pickle
from sentence_transformers import SentenceTransformer
import numpy as np

class TextProcessor:
    def __init__(self, model_name: str = "keepitreal/vietnamese-sbert"):
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.chunks_data = []

    def load_index(self, output_dir: str):
        self.index = faiss.read_index(os.path.join(output_dir, 'embeddings.index'))
        with open(os.path.join(output_dir, 'chunks.pkl'), 'rb') as f:
            self.chunks_data = pickle.load(f)
    
    def search(self, query: str, k: int = 5):
        query_vector = self.model.encode([query])[0].reshape(1, -1)
        distances, indices = self.index.search(query_vector.astype(np.float32), k)
        
        results = []
        for idx, distance in zip(indices[0], distances[0]):
            if idx != -1:
                chunk_data = self.chunks_data[idx]
                results.append({
                    'text': chunk_data['text'],
                    'source': chunk_data['source'],
                    'position': chunk_data['position'],
                    'distance': float(distance)
                })
        
        return results

if __name__ == "__main__":
    output_dir = "vector_db"
    processor = TextProcessor()
    
    print("Loading vector database...")
    processor.load_index(output_dir)
    
    query = "Quy đổi điểm IELTS như thế nào"
    print(f"Searching for: {query}")
    
    results = processor.search(query, k=3)
    print("\nSearch results:")
    for result in results:
        print(f"\nFile: {result['source']}")
        print(f"Text: {result['text'][:]}")  
        print(f"Distance: {result['distance']:.4f}")
