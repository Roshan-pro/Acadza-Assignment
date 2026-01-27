import random
import re
from backend_src.prompt import prompt
from backend_src.ai_factory import llm
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
class Generate_follow_up:
    def __init__(self, user_input: str)->str:
        self.user_input = user_input

    def generate(self)->str:
        try:
            words = re.findall(r'\b\w+\b', self.user_input)
            words = [w for w in words if len(w) >=3]
            chosen_word = random.choice(words) if words else self.user_input.split()[0]
            
            chain =prompt| llm
            response = chain.invoke({
                "user_input": self.user_input,
                "word": chosen_word
            })
            
            return _clean_out(response.content)
        except Exception as e:
            return f"Error generating follow-up question: {str(e)}"
        
def _clean_out(text: str)-> str:
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
    text = re.sub(r"\*\*|\*|`", "", text) 
    text = re.sub(r"\s+", " ", text)  # Normalize whitespace
    return text.strip()