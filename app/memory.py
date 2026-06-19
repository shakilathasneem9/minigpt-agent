import json
import os
from datetime import datetime

FILE_PATH = "chat_memory.json"
MAX_MEMORY = 20  # keep only last 20 chats


def load_memory():
    """Load chat history safely from JSON file"""
    if not os.path.exists(FILE_PATH):
        return []

    try:
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Ensure it's always a list
        if not isinstance(data, list):
            return []

        return data

    except (json.JSONDecodeError, IOError):
        return []


def save_memory(data):
    """Save chat history to JSON file safely"""
    try:
        with open(FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except IOError:
        pass  # fail silently (prevents app crash)


def add_chat(user_query, bot_response):
    """Add new chat entry to memory"""

    memory = load_memory()

    memory.append({
        "user": user_query,
        "assistant": bot_response,
        "time": datetime.now().strftime("%H:%M:%S")
    })

    # Keep memory limited (important for performance + prompt size control)
    memory = memory[-MAX_MEMORY:]

    save_memory(memory)


def get_recent_memory(n=5):
    """Get last n chats (useful for prompt context)"""
    memory = load_memory()
    return memory[-n:]


def clear_memory():
    """Clear all chat history"""
    save_memory([])