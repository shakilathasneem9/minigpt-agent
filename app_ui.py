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
    <h1 style="text-align:center;">🤖 MiniGPT</h1>
    <p style="text-align:center;color:gray;">Your Simple AI Agent</p>
    """,
    unsafe_allow_html=True
)

st.divider()


# =====================================================
# CHAT HISTORY
# =====================================================
for msg in st.session_state.messages:
    avatar = "👤" if msg["role"] == "user" else "🤖"

    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])


# =====================================================
# INPUT
# =====================================================
user_input = st.chat_input("Ask anything to MiniGPT...")


# =====================================================
# PROCESS INPUT
# =====================================================
if user_input:

    # Prevent empty spam
    if user_input.strip() == "":
        st.stop()

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)

    # Assistant response placeholder
    with st.chat_message("assistant", avatar="🤖"):
        placeholder = st.empty()
        placeholder.markdown("🤔 Thinking...")

        try:
            response = requests.post(
                "http://127.0.0.1:8000/chat",
                json={"query": user_input},
                timeout=60
            )

            if response.status_code == 200:
                answer = response.json().get("response", "No response")
            else:
                answer = f"Server Error ({response.status_code})"

        except Exception as e:
            answer = f"Unable to connect to backend.\n\nDetails: {e}"

        placeholder.markdown(answer)

    # Save assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": f"{answer}\n\n🕒 {datetime.now().strftime('%H:%M')}"
    })

    # Single rerun only
    st.rerun()