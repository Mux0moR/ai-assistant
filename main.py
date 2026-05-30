import os
import asyncio
from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import ollama
import chromadb
from chromadb.utils import embedding_functions
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# --- Config ---
MODEL_NAME = os.getenv("MODEL_NAME", "gemma4:e4b")
EMBED_MODEL = os.getenv("EMBED_MODEL", "nomic-embed-text")
KNOWLEDGE_DIR = "knowledge"
DB_DIR = "data"

# --- ChromaDB Setup ---
chroma_client = chromadb.PersistentClient(path=DB_DIR)
# Using Ollama for embeddings
class OllamaEmbeddingFunction(embedding_functions.EmbeddingFunction):
    def __call__(self, input: List[str]) -> List[List[float]]:
        embeddings = []
        for text in input:
            response = ollama.embeddings(model=EMBED_MODEL, prompt=text)
            embeddings.append(response["embedding"])
        return embeddings

emb_fn = OllamaEmbeddingFunction()
collection = chroma_client.get_or_create_collection(
    name="googy_ai_pro_knowledge", 
    embedding_function=emb_fn
)

# --- Document Processing ---
def process_documents():
    if not os.path.exists(KNOWLEDGE_DIR):
        os.makedirs(KNOWLEDGE_DIR)
        return

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    
    for filename in os.listdir(KNOWLEDGE_DIR):
        file_path = os.path.join(KNOWLEDGE_DIR, filename)
        if filename.endswith(".pdf"):
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
        elif filename.endswith(".txt") or filename.endswith(".md"):
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
        else:
            continue

        chunks = text_splitter.split_text(text)
        
        # Add to collection
        ids = [f"{filename}_{i}" for i in range(len(chunks))]
        metadatas = [{"source": filename} for _ in range(len(chunks))]
        
        collection.upsert(
            ids=ids,
            documents=chunks,
            metadatas=metadatas
        )
    print(f"[*] База знаний обновлена. Проиндексировано файлов: {len(os.listdir(KNOWLEDGE_DIR))}")

# --- API Models ---
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    answer: str
    sources: List[str]

# --- Endpoints ---

@app.on_event("startup")
async def startup_event():
    # Запускаем индексацию при старте
    process_documents()

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    # 1. Поиск контекста
    results = collection.query(
        query_texts=[request.message],
        n_results=3
    )
    
    context = "\n\n".join(results["documents"][0])
    sources = list(set([m["source"] for m in results["metadatas"][0]]))
    
    # 2. Промпт для LLM
    prompt = f"""Используй предоставленный контекст, чтобы ответить на вопрос. 
Если в контексте нет ответа, скажи, что ты не знаешь. 
Ориентируйся только на предоставленную информацию.

КОНТЕКСТ:
{context}

ВОПРОС:
{request.message}

ОТВЕТ:"""

    try:
        response = await asyncio.to_thread(
            ollama.generate, 
            model=MODEL_NAME, 
            prompt=prompt
        )
        return ChatResponse(answer=response["response"], sources=sources)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Mount static files
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
