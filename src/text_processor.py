import os
from tqdm import tqdm
import faiss
import pickle
from sentence_transformers import SentenceTransformer
import numpy as np

class TextProcessor:
    def __init__(self, model_name: str = "keepitreal/vietnamese-sbert"):
        self.model = SentenceTransformer(model_name)
        self.chunk_size = 512
        self.overlap = 50
        self.index = None
        self.chunks_data = []
        
    def read_text_file(self, file_path: str) -> str:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def create_chunks(self, text: str, source_file: str):
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), self.chunk_size - self.overlap):
            chunk = ' '.join(words[i:i + self.chunk_size])
            if chunk:
                chunks.append({
                    'text': chunk,
                    'source': source_file,
                    'position': i
                })
        
        return chunks
    
    def process_directory(self, directory_path: str):
        for filename in tqdm(os.listdir(directory_path)):
            if filename.endswith('.txt'):
                file_path = os.path.join(directory_path, filename)
                text = self.read_text_file(file_path)
                chunks = self.create_chunks(text, filename)
                self.chunks_data.extend(chunks)
    
    def create_embeddings(self):
        texts = [chunk['text'] for chunk in self.chunks_data]
        sources = [chunk['source'] for chunk in self.chunks_data]  # Lấy tên file gốc
        
        embeddings = []
        
        print("Creating embeddings...")
        for text, source in tqdm(zip(texts, sources), total=len(texts)):
            embedding = self.model.encode([text])[0]
            embeddings.append(embedding)
            print(f"Embedding created for file: {source}")
        
        embeddings = np.array(embeddings)
        
        # Initialize FAISS index
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index = faiss.IndexIDMap(self.index)
        
        # Add vectors to index
        self.index.add_with_ids(
            embeddings.astype(np.float32),
            np.array(range(len(embeddings))).astype(np.int64)
        )
        
    def save_index(self, output_dir: str):
        os.makedirs(output_dir, exist_ok=True)
        
        # Save FAISS index
        faiss.write_index(self.index, os.path.join(output_dir, 'embeddings.index'))
        
        # Save chunks data
        with open(os.path.join(output_dir, 'chunks.pkl'), 'wb') as f:
            pickle.dump(self.chunks_data, f)

if __name__ == "__main__":
    input_dir = "../CrawlData/data_crawl"
    output_dir = "vector_db"
    
    processor = TextProcessor()
    
    print("Processing text files...")
    processor.process_directory(input_dir)
    
    print("Creating embeddings...")
    processor.create_embeddings()
    
    print("Saving vector database...")
    processor.save_index(output_dir)
    print("Vector database created successfully!")
