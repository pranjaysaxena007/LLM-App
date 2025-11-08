import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

if st.button("🏠 Back to Home"):
    st.switch_page("main.py")

st.markdown("---")

st.title("💬 Chat Assistant")

def chat_with_gemini():
    """Chat with Gemini AI"""
    st.subheader("Talk with AI")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    
    # Chat input
    if user_input := st.chat_input("Type your message:"):
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        with st.chat_message("user"):
            st.write(user_input)
        
        # Get AI response
        with st.spinner("Thinking..."):
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(user_input)
            
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
            with st.chat_message("assistant"):
                st.write(response.text)

chat_with_gemini()

# Navigation footer
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🏠 Home"):
        st.switch_page("main.py")
with col2:
    if st.button("← Previous"):
        st.switch_page("pages/4_document_summarizer.py")
with col3:
    if st.button("Next →"):
        st.switch_page("pages/6_translation_tool.py")
