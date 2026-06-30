from fastapi import FastAPI
from pydantic import BaseModel
import logging

from app.agent import run_agent


# -----------------------------
# LOGGING
# -----------------------------
logging.basicConfig(level=logging.INFO)


# -----------------------------
# APP
# -----------------------------
app = FastAPI(
    title="AI Tool-Augmented Agent",
    description="AI agent with memory, tools, and intent detection",
    version="1.1"
)


# -----------------------------
# REQUEST MODEL
# -----------------------------
class ChatRequest(BaseModel):
    query: str
    user_id: str = "default"


# -----------------------------
# HEALTH CHECK
# -----------------------------
@app.get("/")
def home():
    return {
        "status": "running",
        "message": "AI Agent API is active 🚀"
    }


# -----------------------------
# CHAT ENDPOINT
# -----------------------------
@app.post("/chat")
def chat(request: ChatRequest):

    try:
        logging.info(f"[{request.user_id}] {request.query}")

        response = run_agent(request.query, request.user_id)

        return {
            "success": True,
            "user_id": request.user_id,
            "query": request.query,
            "response": response
        }

    except Exception as e:
        logging.error(f"Error: {str(e)}")

        return {
            "success": False,
            "query": request.query,
            "response": "Something went wrong."
        }