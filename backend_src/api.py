from fastapi import FastAPI,WebSocket
import sys
import os

import uvicorn
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from fastapi.middleware.cors import CORSMiddleware
from backend_src.follow_up import Generate_follow_up
app = FastAPI(
    terms_of_service='ACADZA Assignment',
    title='ACADZA Assignment API',
    description='API for ACADZA Assignment',
    version='1.0.0'
              )
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
async def root():
    return {"message": "Welcome to the ACADZA Assignment API"}
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    count = 0
    last_message = ""
    
    while True:
        user_message = await websocket.receive_text()
        last_message = user_message
        
        if count < 3:
            followup = Generate_follow_up(last_message).generate()
            await websocket.send_text(followup)
            count += 1
        else:
            await websocket.send_text("Thanks, we have got your data.")
            await websocket.close()
            break
if __name__ == "__main__":
    uvicorn.run(
        "backend_src.api:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )

#uvicorn backend_src.api:app --reload