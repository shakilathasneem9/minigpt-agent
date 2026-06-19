import re


def is_math_expression(text: str) -> bool:
    """
    Strict math detection:
    only allows clean arithmetic expressions
    """
    text = text.strip()

    # Pure math like: 2+2, 10 * 5, (2+3)/5
    pattern = r"^[0-9\s\+\-\*\/\(\)\.]+$"

    return bool(re.match(pattern, text))


def classify_intent(query: str) -> str:
    """
    Rule-based intent classifier (stable + production-safe)
    """

    q = query.lower().strip()

    # -------------------------
    # 1. MATH (HIGHEST PRIORITY)
    # -------------------------
    if is_math_expression(q):
        return "math"

    if any(word in q for word in ["calculate", "solve", "compute"]):
        return "math"

    # -------------------------
    # 2. SEARCH INTENT
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
    # 3. GENERAL (DEFAULT)
    # -------------------------
    return "general"