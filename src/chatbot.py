from typing import List, Tuple
import google.generativeai as genai

class Chatbot:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        instruction = """You are a helpful chatbot that provides information and advice about admission to the University of Information Technology (UIT). You should strive to provide clear, detailed, and relevant responses to user queries based on the information available in your database. If the user's question is not directly covered by the database, you can supplement your response with general information about UIT or by searching the internet for relevant details."""
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp', system_instruction=instruction)
        
    def generate_response(self, query: str, relevant_qa: List[Tuple[str, str, float, List[dict]]]) -> str:
        context = ""
        for question, answer, bm25_score, vector_results in relevant_qa:
            context += f"Q: {question}\nA: {answer}\nBM25 Score: {bm25_score:.2f}\n"
            for vector_result in vector_results:
                context += f"Relevant Passage: {vector_result['text']}\nSource: {vector_result['source']}\nDistance: {vector_result['distance']:.2f}\n"
            context += "\n"
        
        prompt = f"""Question: {query}
        Related information from database:
        {context}
        
        Please provide a helpful response based on the above information. If the question isn't directly related to the provided information, you can provide a general response."""
        
        response = self.model.generate_content(prompt)
        return response.text