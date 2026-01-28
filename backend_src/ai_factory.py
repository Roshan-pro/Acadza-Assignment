import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from langchain_groq import ChatGroq
from config import api_keys

llm = ChatGroq(
    api_key=api_keys.GROQ_API_KEY, 
    model="qwen/qwen3-32b",
    temperature=0.7)
print("Groq LLM loaded successfully")

