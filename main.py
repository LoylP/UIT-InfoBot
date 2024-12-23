from src.database import init_database, get_qa_data
from src.search_engine import SearchEngine
from src.chatbot import Chatbot
from src.utils import load_api_key

def main():
    print("Initializing database...")
    init_database()
    
    df = get_qa_data()
    
    print("Initializing search engine...")
    search_engine = SearchEngine(
        questions=df['Question'].tolist(),
        answers=df['Answer'].tolist(),
        output_dir="src/vector_db"
    )
    
    print("Initializing chatbot...")
    api_key = load_api_key()
    chatbot = Chatbot(api_key)
    
    while True:
        query = input("\nEnter your question (or 'quit' to exit): ")
        if query.lower() == 'quit':
            break
            
        relevant_qa = search_engine.search(query)
        
        response = chatbot.generate_response(query, relevant_qa)
        print("\nResponse:", response)

if __name__ == "__main__":
    main()