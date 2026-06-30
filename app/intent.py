import re


def is_math_expression(text: str) -> bool:
    text = text.strip()
    pattern = r"^[0-9\s\+\-\*\/\(\)\.]+$"
    return bool(re.match(pattern, text))


def classify_intent(query: str) -> str:

    q = query.lower().strip()

    # -------------------------
    # 1. MATH (HIGHEST PRIORITY)
    # -------------------------
    if is_math_expression(q):
        return "math"

    if any(word in q for word in ["calculate", "solve", "compute"]):
        return "math"

    # -------------------------
    # 2. SEARCH
    # -------------------------
    search_keywords = [
        "latest",
        "news",
        "who is",
        "where is",
        "define",
        "information about"
    ]

    if any(word in q for word in search_keywords):
        return "search"

    # -------------------------
    # 3. MEMORY / FOLLOW-UP INTENT (NEW)
    # -------------------------
    memory_keywords = [
        "what about",
        "tell me more",
        "more about",
        "who is he",
        "who is it",
        "continue",
        "explain more",
        "elaborate"
    ]

    if any(word in q for word in memory_keywords):
        return "memory"

    # -------------------------
    # 4. TOPIC DETECTION (context trigger)
    # -------------------------
    topic_keywords = [
        "football",
        "cricket",
        "python",
        "coding",
        "programming",
        "ai",
        "machine learning"
    ]

    if any(word in q for word in topic_keywords):
        return "general"

    # -------------------------
    # 5. DEFAULT
    # -------------------------
    return "general"