import numpy as np
from rank_bm25 import BM25Okapi
from typing import List, Tuple
from .load_vectorDB import TextProcessor

class SearchEngine:
    def __init__(self, questions: List[str], answers: List[str], output_dir: str):
        self.questions = questions
        self.answers = answers
        
        # Initialize BM25
        tokenized_questions = [q.lower().split() for q in questions]
        self.bm25 = BM25Okapi(tokenized_questions)
        
        # Initialize vector search
        self.text_processor = TextProcessor()
        self.text_processor.load_index(output_dir)

    def search(self, query: str, top_k: int = 3) -> List[Tuple[str, str, float, List[dict]]]:
        # BM25 scores
        tokenized_query = query.lower().split()
        bm25_scores = self.bm25.get_scores(tokenized_query)
        
        # Get top results from BM25
        top_indices = np.argsort(bm25_scores)[-top_k:][::-1]
        bm25_results = []
        for idx in top_indices:
            bm25_results.append((
                self.questions[idx],
                self.answers[idx],
                float(bm25_scores[idx]),
                []
            ))
        
        # Get top results from vector search
        vector_search_results = self.text_processor.search(query, k=top_k)
        
        # Combine results
        results = bm25_results
        for vector_result in vector_search_results:
            results.append((
                vector_result['text'],
                "",
                0.0,
                [vector_result]
            ))
        
        # print("ketqua: ", results)
        return results