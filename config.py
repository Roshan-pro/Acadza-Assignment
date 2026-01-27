import os 
import dotenv
dotenv.load_dotenv()

class api_keys:
    GOOGLE_GEMINI_API_KEY = os.getenv("google_gemini_api_key")
    GROQ_API_KEY = os.getenv("groq_api_key")