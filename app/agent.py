from app.intent import classify_intent
from app.llm import call_llm
from app.tools.search import web_search
from app.tools.calculator import calculate

# ✅ FIXED IMPORT (IMPORTANT)
from app.memory import build_prompt, add_chat, add_memory


# -----------------------------
# TOOL WRAPPERS
# -----------------------------

def handle_search(query: str):
    try:
        return web_search(query) or ""
    except Exception as e:
        print("Search error:", e)
        return ""


def handle_math(query: str):
    try:
        return calculate(query) or ""
    except Exception as e:
        print("Math error:", e)
        return ""


# -----------------------------
# INTENT HANDLING
# -----------------------------

def safe_intent(query: str):
    try:
        intent = classify_intent(query)
    except Exception as e:
        print("Intent error:", e)
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
# MAIN AGENT PIPELINE
# -----------------------------

def run_agent(query: str, user_id: str = "default"):

    try:
        # 1. intent detection
        intent = safe_intent(query)

        # 2. tool execution
        tool_context = run_tool(intent, query)

        # 3. build prompt with memory
        prompt = build_prompt(query)

        # 4. attach tool result
        if tool_context:
            prompt += f"\n\nTool Context:\n{tool_context}"

        # 5. LLM CALL (Groq)
        response = call_llm(
            system_prompt="You are MiniGPT, a helpful AI assistant.",
            user_prompt=prompt
        )

        # 6. save short-term memory
        add_chat(query, response)

        # 7. save long-term memory (optional smart storage)
        if any(x in query.lower() for x in ["i like", "i love", "i am", "my name"]):
            add_memory(query)

        return response

    except Exception as e:
        import traceback
        traceback.print_exc()
        return f"ERROR IN AGENT: {str(e)}"


# -----------------------------
# TEST
# -----------------------------

if __name__ == "__main__":
    print(run_agent("I like football"))