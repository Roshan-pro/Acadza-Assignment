from langchain_core.prompts import ChatPromptTemplate

prompt =ChatPromptTemplate([
    ("system", 
     "You are an AI assistant. "
     "Generate ONLY ONE follow-up question. "
     "The question MUST contain the exact word: '{word}'."),
    
    ("human", "User input: {user_input}\n\nFollow-up question:")
])
    