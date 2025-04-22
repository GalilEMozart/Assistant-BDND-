import os 
import gc
import sys
import atexit
import multiprocessing
from contextlib import asynccontextmanager

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from src.rag import RAG

def cleanup_resources():
    if hasattr(multiprocessing, 'resource_tracker'):
        multiprocessing.resource_tracker._resource_tracker.clear()

assistant = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """ Action lors du démarrage et de l'arrêt de l'application (liberer propremet le gpu)"""
    
    global assistant
    assistant = RAG()
    yield

    print('feremture process')
    
    assistant.close()
    del assistant
    gc.collect()  

app = FastAPI(lifespan=lifespan)


# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # ou ["*"] si tu veux tout autoriser (dev seulement)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str

@app.get("/")
def health_check():
    """ check if the api works """
    
    return {"status": "ok"}

@app.post("/ask")
def ask_bdnb(request: QueryRequest):
    """ query to llm agent """
    try:
        answer = assistant.run(request.question)
        return {"question": request.question, "answer": answer}
    except Exception as e:
        return {"error": str(e)}

