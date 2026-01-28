import streamlit as st
import websocket
import json

st.set_page_config(page_title="ACADZA Assignment", layout="centered")
st.title("🤖 AI Follow-Up Assistant")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "ws" not in st.session_state:
    st.session_state.ws = None
if "conversation_step" not in st.session_state:
    st.session_state.conversation_step = 0  # 0: initial, 1-3: follow-ups, 4: done
if "current_input" not in st.session_state:
    st.session_state.current_input = ""

# Display chat history
for message in st.session_state.messages:
    if message["type"] == "ai":
        st.markdown(f"**🤖 AI:** {message['content']}")
    else:
        st.markdown(f"**👤 You:** {message['content']}")

# Main conversation logic
if st.session_state.conversation_step == 0:
    # Initial input
    user_input = st.text_input("Enter your initial sentence:", key="initial_input")
    
    if st.button("Launch") and user_input:
        try:
            # Connect to WebSocket
            ws = websocket.WebSocket()
            ws.connect("wss://acadza-assignment-3.onrender.com/ws", timeout=10)#ws://localhost:8000/ws
            st.session_state.ws = ws
            
            # Receive welcome message
            welcome = st.session_state.ws.recv()
            st.session_state.messages.append({"type": "ai", "content": welcome})
            
            # Send initial message
            st.session_state.ws.send(user_input)
            st.session_state.messages.append({"type": "user", "content": user_input})
            
            # Receive first follow-up
            followup1 = st.session_state.ws.recv()
            st.session_state.messages.append({"type": "ai", "content": followup1})
            
            st.session_state.conversation_step = 1
            st.rerun()
            
        except Exception as e:
            st.error(f"Connection error: {e}")

elif 1 <= st.session_state.conversation_step <= 3:
    # Follow-up answers
    answer_key = f"answer_{st.session_state.conversation_step}"
    
    with st.form(key=f"form_{st.session_state.conversation_step}"):
        user_answer = st.text_input(f"Your answer to follow-up #{st.session_state.conversation_step}:", 
                                   key=answer_key)
        submit = st.form_submit_button("Submit Answer")
        
        if submit and user_answer:
            try:
                # Send answer
                st.session_state.ws.send(user_answer)
                st.session_state.messages.append({"type": "user", "content": user_answer})
                
                # Receive next follow-up (if not the last one)
                if st.session_state.conversation_step < 3:
                    followup = st.session_state.ws.recv()
                    if "Thanks" not in followup:
                        st.session_state.messages.append({"type": "ai", "content": followup})
                        st.session_state.conversation_step += 1
                    else:
                        st.session_state.messages.append({"type": "ai", "content": followup})
                        st.session_state.conversation_step = 4
                else:
                    # After 3rd answer, receive final message
                    final_msg = st.session_state.ws.recv()
                    st.session_state.messages.append({"type": "ai", "content": final_msg})
                    st.session_state.conversation_step = 4
                
                st.rerun()
                
            except Exception as e:
                st.error(f"Error: {e}")

elif st.session_state.conversation_step == 4:
    # Conversation complete
    st.balloons()
    st.success("🎉 Conversation completed!")
    
    if st.button("Start New Conversation"):
        # Clean up WebSocket
        if st.session_state.ws:
            try:
                st.session_state.ws.close()
            except:
                pass
        
        # Reset session state
        for key in ["messages", "ws", "conversation_step", "current_input"]:
            if key in st.session_state:
                del st.session_state[key]
        
        st.rerun()

# WebSocket cleanup on page unload
if st.session_state.ws and st.session_state.conversation_step == 4:
    try:
        st.session_state.ws.close()
        st.session_state.ws = None
    except:
        pass