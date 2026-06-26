import streamlit as st
import requests
from datetime import datetime
from pathlib import Path

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="MiniGPT",
    page_icon="🤖",
    layout="centered"
)

# =====================================================
# LOAD CSS
# =====================================================
css_file = Path(__file__).parent / "style.css"

if css_file.exists():
    st.markdown(
        f"<style>{css_file.read_text(encoding='utf-8')}</style>",
        unsafe_allow_html=True
    )

# =====================================================
# SESSION STATE
# =====================================================
if "messages" not in st.session_state:
    st.session_state.messages = []

# =====================================================
# SIDEBAR
# =====================================================
with st.sidebar:

    st.header("⚙️ Settings")

    response_style = st.selectbox(
        "Response Style",
        ["Balanced", "Concise", "Detailed"]
    )

    st.divider()

    st.caption("MiniGPT v1.0")

# =====================================================
# HEADER
# =====================================================
st.markdown(
    """
    <h1 style="text-align:center;">
        🤖 MiniGPT
    </h1>

    <p style="text-align:center;color:gray;">
        Your Simple AI Agent
    </p>
    """,
    unsafe_allow_html=True
)

st.divider()

# =====================================================
# CHAT HISTORY
# =====================================================
chat_container = st.container()

with chat_container:

    for msg in st.session_state.messages:

        avatar = "👤" if msg["role"] == "user" else "🤖"

        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

# =====================================================
# CHAT INPUT
# =====================================================
text_input = st.chat_input(
    "Ask anything to MiniGPT..."
)

# =====================================================
# GET USER INPUT
# =====================================================
user_input = None

if text_input:
    user_input = text_input
# =====================================================
# PROCESS MESSAGE
# =====================================================

if user_input:

    # Add user message immediately
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # Rerender user message instantly
    with chat_container:
        with st.chat_message("user", avatar="👤"):
            st.markdown(user_input)

    # Show thinking bubble
    with chat_container:
        with st.chat_message("assistant", avatar="🤖"):

            thinking_placeholder = st.empty()
            thinking_placeholder.markdown("🤔 Thinking...")

            try:

                response = requests.post(
                    "http://127.0.0.1:8000/chat",
                    json={
                        "query": user_input,
                        "style": response_style
                    },
                    timeout=60
                )

                if response.status_code == 200:

                    answer = response.json().get(
                        "response",
                        "No response"
                    )

                else:

                    answer = (
                        f"Server Error "
                        f"({response.status_code})"
                    )

            except Exception as e:

                answer = (
                    "Unable to connect to backend.\n\n"
                    f"Details: {e}"
                )

            # Replace thinking with answer
            thinking_placeholder.empty()

            st.markdown(answer)

    final_answer = (
        f"{answer}\n\n"
        f"🕒 {datetime.now().strftime('%H:%M')}"
    )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": final_answer
        }
    )

    st.rerun()
    st.rerun()