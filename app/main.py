from fastapi import FastAPI
from pydantic import BaseModel
import logging

from app.agent import run_agent


# -----------------------------
# Logging setup
# -----------------------------
logging.basicConfig(level=logging.INFO)


# -----------------------------
# FastAPI app
# -----------------------------
app = FastAPI(
    title="AI Tool-Augmented Agent",
    description="An AI agent with intent detection and tool usage",
    version="1.0"
)


# -----------------------------
# Request schema
# -----------------------------
class ChatRequest(BaseModel):
    query: str


# -----------------------------
# Health check
# -----------------------------
@app.get("/")
def home():
    return {
        "status": "running",
        "message": "AI Agent API is active 🚀"
    }


# -----------------------------
# Main chat endpoint
# -----------------------------
@app.post("/chat")
def chat(request: ChatRequest):
    try:
        logging.info(f"User query: {request.query}")

        response = run_agent(request.query)

        return {
            "success": True,
            "query": request.query,
            "response": response
        }

    except Exception as e:
        logging.error(f"Error in /chat: {str(e)}")

        return {
            "success": False,
            "query": request.query,
            "response": "Sorry, something went wrong while processing your request."
        }