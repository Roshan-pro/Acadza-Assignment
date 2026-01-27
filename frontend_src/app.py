import streamlit as st
import websocket

st.set_page_config(page_title="ACADZA Assignment API", layout="centered")
st.title("🤖 AI Follow-Up Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "ws" not in st.session_state:
    st.session_state.ws = None

user_input = st.text_input("Enter a sentence:")

if st.button("Launch"):
    st.session_state.ws = websocket.WebSocket()
    st.session_state.ws.connect("ws://localhost:8000/ws")
    st.session_state.ws.send(user_input)

while st.session_state.ws:
    try:
        reply = st.session_state.ws.recv()
        st.session_state.messages.append(reply)
        st.session_state.ws.send(st.text_input("Your answer:", key=len(st.session_state.messages)))
    except:
        break

for msg in st.session_state.messages:
    st.markdown(f"**AI:** {msg}")
