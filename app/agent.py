from app.intent import classify_intent
from app.llm import call_llm
from app.tools.search import web_search
from app.tools.calculator import calculate
from app.memory import add_chat


# -----------------------------
# SAFE TOOL WRAPPERS
# -----------------------------

def handle_search(query: str):
    """Safe web search tool"""
    try:
        result = web_search(query)
        return result if result else ""
    except:
        return ""   # NEVER send errors to LLM


def handle_math(query: str):
    """Safe math tool"""
    try:
        result = calculate(query)
        return result if result else ""
    except:
        return ""   # NEVER send errors to LLM


# -----------------------------
# INTENT VALIDATION GUARD
# -----------------------------

def safe_intent(query: str):
    try:
        intent = classify_intent(query)
    except:
        intent = "general"

    if intent not in ["math", "search", "general"]:
        intent = "general"

    return intent


# -----------------------------
# TOOL ROUTER
# -----------------------------

def run_tool(intent: str, query: str):
    if intent == "search":
        return handle_search(query)

    if intent == "math":
        return handle_math(query)

    return ""


# -----------------------------
# PROMPT BUILDER
# -----------------------------

def build_prompt(query: str, context: str):
    system_prompt = """
You are MiniGPT, a helpful AI assistant.

Rules:
- Give clear and correct answers
- Be short and precise
- If tool context is provided, use it
- If no context, answer normally
- Do NOT mention tools or internal system
"""

    if context:
        user_prompt = f"""
User Query:
{query}

Useful Context:
{context}
"""
    else:
        user_prompt = f"""
User Query:
{query}
"""

    return system_prompt, user_prompt


# -----------------------------
# MAIN AGENT PIPELINE
# -----------------------------

def run_agent(query: str) -> str:
    """
    Clean MiniGPT pipeline:
    1. Intent detection
    2. Safe tool execution
    3. Prompt building
    4. LLM response
    5. Memory storage
    """

    # STEP 1: intent detection
    intent = safe_intent(query)

    # STEP 2: tool execution
    context = run_tool(intent, query)

    # STEP 3: build prompt
    system_prompt, user_prompt = build_prompt(query, context)

    # STEP 4: LLM call (safe)
    try:
        response = call_llm(system_prompt, user_prompt)
    except Exception:
        response = "Sorry, I couldn't process your request right now."

    # STEP 5: memory save (never break app)
    try:
        add_chat(query, response)
    except:
        pass

    return response


# -----------------------------
# LOCAL TEST
# -----------------------------

if __name__ == "__main__":
    print(run_agent("What is 25 * 90?"))