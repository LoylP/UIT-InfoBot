from fastapi import FastAPI
from pydantic import BaseModel
from src.database import init_database, get_qa_data
from src.search_engine import SearchEngine
from src.chatbot import Chatbot
from src.utils import load_api_key

app = FastAPI()

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

class QueryRequest(BaseModel):
    query: str

@app.get("/")
async def read_root():
    return {"message": "Welcome to the chatbot API!"}

# endpoint get input_query
@app.post("/ask")
async def ask_question(request: QueryRequest):
    query = request.query
    if query.lower() == 'quit':
        return {"message": "Exiting chatbot."}
    
    relevant_qa = search_engine.search(query)
    response = chatbot.generate_response(query, relevant_qa)
    return {"response": response}

if __name__== "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)

