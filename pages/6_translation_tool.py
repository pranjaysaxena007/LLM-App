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

st.title("🌐 Translation Tool")

def translate_text():
    """Translate text using Gemini API"""
    st.subheader("Translate Text")
    
    languages = ["Spanish", "French", "German", "Japanese", "Chinese", "Hindi", "Arabic"]
    target_lang = st.selectbox("Target language:", languages)
    
    text = st.text_area("Text to translate:")
    
    if st.button("Translate", type="primary"):
        if text:
            model = genai.GenerativeModel('gemini-pro')
            prompt = f"Translate to {target_lang}: {text}"
            response = model.generate_content(prompt)
            st.write(response.text)

translate_text()

# Navigation footer
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🏠 Home"):
        st.switch_page("main.py")
with col2:
    if st.button("← Previous"):
        st.switch_page("pages/5_chat_assistant.py")
with col3:
    if st.button("Next →"):
        st.switch_page("pages\7_calorie_counter.py")
