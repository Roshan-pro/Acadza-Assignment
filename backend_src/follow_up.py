import random
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
            words = [w for w in self.user_input.split() if len(w) > 4]
            chosen_word = random.choice(words) if words else self.user_input.split()[0]
            
            chain =prompt| llm
            response = chain.invoke({
                "user_input": self.user_input,
                "word": chosen_word
            })
            
            return response.content.strip()
        except Exception as e:
            return f"Error generating follow-up question: {str(e)}"