from fastapi import FastAPI,WebSocket, WebSocketDisconnect
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

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        await websocket.send_text("Connection established. You can start sending messages.")
        
        first_message= await websocket.receive_text()
        follow_up_generator = Generate_follow_up(first_message)
        follow_up_question1 = follow_up_generator.generate()
        await websocket.send_text(f'1. {follow_up_question1}')
        
        aswer1 = await websocket.receive_text()
        follow_up_generator = Generate_follow_up(aswer1)
        follow_up_question2 = follow_up_generator.generate()
        await websocket.send_text(f'2. {follow_up_question2}')

        aswer2 = await websocket.receive_text()
        follow_up_generator = Generate_follow_up(aswer2)
        follow_up_question3 = follow_up_generator.generate()
        await websocket.send_text(f'3. {follow_up_question3}')
        
        aswer3 = await websocket.receive_text()

        await websocket.send_text("Thanks, we have got your data.")
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        await websocket.send_text(f"Error: {str(e)}")
    finally:
        try:
            await websocket.close() 
        except:
            pass

if __name__ == "__main__":
    uvicorn.run(
        "backend_src.api:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

#uvicorn backend_src.api:app --reload