# backend/llm_client.py
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

_api_key = os.getenv("GROQ_API_KEY")
if not _api_key:
    raise RuntimeError("GROQ_API_KEY not set in .env")

client = Groq(api_key=_api_key)

def call_llm(system_prompt: str, user_message: str, temperature: float = 0.3) -> str:
    """
    Generic wrapper for Groq Llama 3.1 models.
    """
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",   # ⭐ Free, fast, and perfect for your project
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        temperature=temperature,
    )
    return response.choices[0].message.content
