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

st.title("📄 Document Summarizer")

def summarize_document():
    """Summarize documents using Gemini API"""
    st.subheader("Summarize Your Content")
    
    text = st.text_area("Paste your document text:", height=150)
    summary_length = st.selectbox("Summary length:", ["Short", "Medium", "Long"])
    
    if st.button("Summarize", type="primary"):
        if text:
            model = genai.GenerativeModel('gemini-pro')
            prompt = f"Summarize this {summary_length.lower()}: {text}"
            response = model.generate_content(prompt)
            st.write(response.text)

summarize_document()

# Navigation footer
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🏠 Home"):
        st.switch_page("main.py")
with col2:
    if st.button("← Previous"):
        st.switch_page("pages/3_code_generator.py")
with col3:
    if st.button("Next →"):
        st.switch_page("pages/5_chat_assistant.py")
