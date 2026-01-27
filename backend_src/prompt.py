from langchain_core.prompts import ChatPromptTemplate

prompt =ChatPromptTemplate.from_messages([
    ("system", 
     "You are an AI assistant designed to generate thoughtful follow-up questions. "
     "Generate ONLY ONE follow-up question based on the user's input. "
     "The question MUST contain the exact word: '{word}'. "
     "Make the question natural, conversational, and relevant to what the user said. "
     "Do not add any explanations, just output the question."),
    
    ("human", "User said: {user_input}\n\nGenerate a follow-up question:")
])