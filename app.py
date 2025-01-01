from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.database import init_database, get_qa_data, save_history, get_history
from src.search_engine import SearchEngine
from src.chatbot import Chatbot
from src.utils import load_api_key

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

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
@app.get("/ask")
async def ask_question(query: str):
    if query.lower() == 'quit':
        return {"message": "Exiting chatbot."}
    
    relevant_qa, sources = search_engine.search(query)
    response = chatbot.generate_response(query, relevant_qa)

    save_history(query, response, sources)

    return {"response": response}

# endpoint get history of user_chat and chatbot_response
@app.get("/history")
async def show_history():
    history = get_history()
    return history.to_dict(orient="records")

if __name__== "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)

