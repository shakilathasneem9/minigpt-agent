import json
import os
import numpy as np
from datetime import datetime
from sentence_transformers import SentenceTransformer

# =========================
# CONFIG
# =========================

CHAT_FILE = "chat_memory.json"
MEMORY_FILE = "memory.json"
MAX_CHAT = 20

model = SentenceTransformer("all-MiniLM-L6-v2")


# =========================
# FILE HELPERS
# =========================

def load_json(path):
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except:
        return []


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# =========================
# EMBEDDINGS
# =========================

def embed(text: str):
    return model.encode(text)


def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


# =========================
# SHORT TERM MEMORY
# =========================

def add_chat(user_msg: str, assistant_msg: str):
    chat = load_json(CHAT_FILE)

    chat.append({
        "user": user_msg,
        "assistant": assistant_msg,
        "time": str(datetime.now())
    })

    chat = chat[-MAX_CHAT:]
    save_json(CHAT_FILE, chat)


def get_chat():
    return load_json(CHAT_FILE)


# =========================
# LONG TERM MEMORY
# =========================

def add_memory(text: str):
    memory = load_json(MEMORY_FILE)

    memory.append({
        "text": text,
        "vector": embed(text).tolist(),
        "time": str(datetime.now()),
        "weight": 1.0
    })

    save_json(MEMORY_FILE, memory)


def get_memory():
    return load_json(MEMORY_FILE)


# =========================
# SMART SEARCH
# =========================

def search_memory(query: str, memories, top_k=5):
    if not memories:
        return []

    q_vec = embed(query)

    scored = []
    for m in memories:
        score = cosine_similarity(q_vec, m["vector"]) * m.get("weight", 1.0)
        scored.append((score, m))

    scored.sort(reverse=True, key=lambda x: x[0])

    return [m for _, m in scored[:top_k]]


# =========================
# MEMORY RULES
# =========================

def should_store(user_msg: str):
    msg = user_msg.lower()

    triggers = [
        "i like",
        "i love",
        "i hate",
        "i am learning",
        "my name is",
        "i am from"
    ]

    return any(t in msg for t in triggers)


# =========================
# PROMPT BUILDER (FIXED)
# =========================

def build_prompt(user_msg: str):
    memories = get_memory()
    chats = get_chat()

    relevant = search_memory(user_msg, memories)

    prompt = "You are a helpful AI assistant with memory.\n\n"

    # LONG TERM MEMORY
    if relevant:
        prompt += "Relevant Memory:\n"
        for m in relevant:
            prompt += f"- {m['text']}\n"
        prompt += "\n"

    # SHORT TERM CHAT
    if chats:
        prompt += "Recent Conversation:\n"
        for c in chats:
            prompt += f"User: {c['user']}\nAssistant: {c['assistant']}\n"
        prompt += "\n"

    prompt += f"User: {user_msg}\nAssistant:"
    return prompt


# =========================
# SAFE WRAPPER (IMPORTANT FIX)
# =========================

def run_memory_pipeline(user_msg: str, llm):
    """
    Correct way to use memory system with LLM
    """

    response = llm(build_prompt(user_msg))

    add_chat(user_msg, response)

    if should_store(user_msg):
        add_memory(user_msg)

    return response