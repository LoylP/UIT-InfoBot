import os
from tqdm import tqdm
import faiss
import pickle
from sentence_transformers import SentenceTransformer
from docx import Document
import numpy as np

class TextProcessor:
    def __init__(self, model_name: str = "keepitreal/vietnamese-sbert"):
        self.model = SentenceTransformer(model_name)
        self.chunk_size = 512
        self.overlap = 50
        self.index = None
        self.chunks_data = []
        self.loaded_index_path = None

    def read_text_file(self, file_path: str) -> str:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    def read_docx_file(self, file_path: str) -> str:
        """Đọc nội dung từ file .docx."""
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])

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
            file_path = os.path.join(directory_path, filename)

            # Xử lý file .txt
            if filename.endswith('.txt'):
                text = self.read_text_file(file_path)
            # Xử lý file .docx
            elif filename.endswith('.docx'):
                text = self.read_docx_file(file_path)
            else:
                continue  # Bỏ qua file không phải .txt hoặc .docx

            chunks = self.create_chunks(text, filename)
            self.chunks_data.extend(chunks)

    def create_embeddings(self):
        texts = [chunk['text'] for chunk in self.chunks_data]
        embeddings = []

        print("Creating embeddings...")
        for text in tqdm(texts):
            embedding = self.model.encode([text])[0]
            embeddings.append(embedding)

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

    def load_index(self, index_dir: str):
        """Load existing FAISS index and chunks data."""
        self.loaded_index_path = index_dir
        index_path = os.path.join(index_dir, 'embeddings.index')
        chunks_path = os.path.join(index_dir, 'chunks.pkl')

        # Load FAISS index
        if os.path.exists(index_path):
            self.index = faiss.read_index(index_path)
        else:
            raise FileNotFoundError(f"Index file not found: {index_path}")

        # Load chunks data
        if os.path.exists(chunks_path):
            with open(chunks_path, 'rb') as f:
                self.chunks_data = pickle.load(f)
        else:
            raise FileNotFoundError(f"Chunks data file not found: {chunks_path}")

    def add_new_data(self, file_path: str):
        """Process new data and add to the FAISS index."""

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        if file_path.endswith('.txt'):
            text = self.read_text_file(file_path)
        elif file_path.endswith('.docx'):
            text = self.read_docx_file(file_path)
        else:
            raise ValueError("Unsupported file format. Only .txt and .docx are allowed.")

        chunks = self.create_chunks(text, os.path.basename(file_path))

        texts = [chunk['text'] for chunk in chunks]
        print("Creating embeddings for new data...")
        new_embeddings = np.array([self.model.encode(text) for text in tqdm(texts)])

        # Gán ID duy nhất cho chunks mới
        start_id = len(self.chunks_data)  # Bắt đầu ID từ kích thước hiện tại của chunks_data
        new_ids = np.arange(start_id, start_id + len(chunks)).astype(np.int64)

        # Cập nhật FAISS index
        self.index.add_with_ids(new_embeddings.astype(np.float32), new_ids)

        # Thêm dữ liệu chunks mới vào chunks_data
        self.chunks_data.extend(chunks)

        print(f"Added {len(chunks)} new chunks from file '{file_path}' to the FAISS index.")


    def save_updated_index(self):
        """Save updated FAISS index and chunks data."""
        if not self.loaded_index_path:
            raise ValueError("Loaded index path not set. Use `load_index` before saving.")
        index_path = os.path.join(self.loaded_index_path, 'embeddings.index')
        chunks_path = os.path.join(self.loaded_index_path, 'chunks.pkl')

        # Save FAISS index
        faiss.write_index(self.index, index_path)

        # Save chunks data
        with open(chunks_path, 'wb') as f:
            pickle.dump(self.chunks_data, f)

        print("Updated vector database saved successfully.")

if __name__ == "__main__":
    # input_dir = "../CrawlData/data_crawl"
    output_dir = "vector_db"

    processor = TextProcessor()

    # Create initial database
    # print("Processing text files...")
    # processor.process_directory(input_dir)

    # print("Creating embeddings...")
    # processor.create_embeddings()

    # print("Saving vector database...")
    # processor.save_index(output_dir)
    # print("Vector database created successfully!")

    # Tải index và dữ liệu chunks
    # print("Loading existing vector database...")
    # processor.load_index(output_dir)
    
    # # Đường dẫn tới tệp mới cần thêm
    # new_file_path = "/home/loylp/project/UIT-InfoBot/data/data.docx"
    # print("Adding new data from file...")
    # processor.add_new_data(new_file_path)

    # # Lưu lại index và chunks sau khi thêm
    # print("Saving updated vector database...")
    # processor.save_updated_index()
    # print("Vector database updated successfully!")
