import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

def call_llm(
    system_prompt: str,
    user_prompt: str,
    model: str = "llama-3.1-8b-instant"
) -> str:
    """
    Groq-powered real AI brain (fast + free tier)
    """

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"LLM Error: {str(e)}"