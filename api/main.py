import os
import uuid
import time
from contextlib import asynccontextmanager
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage

from api.models import SessionLocal, QueryLog, Feedback, create_tables
from rag.chain import get_rag_chain

load_dotenv()

sessions: dict[str, InMemoryChatMessageHistory] = {}
chain = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global chain
    create_tables()
    chain = get_rag_chain()
    yield

app = FastAPI(title="Medical Records RAG API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Schemas ---
class ChatRequest(BaseModel):
    question: str
    session_id: str | None = None

class ChatResponse(BaseModel):
    answer: str
    session_id: str
    query_log_id: str
    sources: list[str]

class FeedbackRequest(BaseModel):
    query_log_id: str
    rating: int
    comment: str | None = None

class FeedbackResponse(BaseModel):
    id: str
    message: str

# --- Endpoints ---
@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    session_id = request.session_id or str(uuid.uuid4())

    if session_id not in sessions:
        sessions[session_id] = InMemoryChatMessageHistory()

    history = sessions[session_id]

    start = time.time()
    result = chain.invoke({
        "question": request.question,
        "chat_history": history.messages,
    })
    latency_ms = (time.time() - start) * 1000

    answer = result["answer"]
    source_docs = result.get("source_documents", [])
    sources = [doc.page_content[:150] for doc in source_docs]

    history.add_message(HumanMessage(content=request.question))
    history.add_message(AIMessage(content=answer))

    query_log_id = str(uuid.uuid4())
    db = SessionLocal()
    try:
        log = QueryLog(
            id=query_log_id,
            session_id=session_id,
            question=request.question,
            answer=answer,
            retrieval_mode="hybrid",
            num_sources=len(source_docs),
            latency_ms=latency_ms,
        )
        db.add(log)
        db.commit()
    finally:
        db.close()

    return ChatResponse(
        answer=answer,
        session_id=session_id,
        query_log_id=query_log_id,
        sources=sources,
    )

@app.post("/feedback", response_model=FeedbackResponse)
def feedback(request: FeedbackRequest):
    if request.rating not in [1, 2, 3, 4, 5]:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")

    db = SessionLocal()
    try:
        feedback_id = str(uuid.uuid4())
        fb = Feedback(
            id=feedback_id,
            query_log_id=request.query_log_id,
            rating=request.rating,
            comment=request.comment,
        )
        db.add(fb)
        db.commit()
    finally:
        db.close()

    return FeedbackResponse(id=feedback_id, message="Feedback recorded")

@app.get("/stats")
def stats():
    db = SessionLocal()
    try:
        total_queries = db.query(QueryLog).count()
        avg_latency = db.query(QueryLog).with_entities(QueryLog.latency_ms).all()
        avg_ms = (
            sum(r[0] for r in avg_latency if r[0]) / len(avg_latency)
            if avg_latency else 0
        )
        total_feedback = db.query(Feedback).count()
        return {
            "total_queries": total_queries,
            "avg_latency_ms": round(avg_ms, 2),
            "total_feedback": total_feedback,
        }
    finally:
        db.close()