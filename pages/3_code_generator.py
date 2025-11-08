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

st.title("💻 Code Generator")

def generate_code_with_gemini():
    """Generate code using Gemini API"""
    st.subheader("Generate Code")
    
    language = st.selectbox("Language:", ["Python", "JavaScript", "Java", "C++", "SQL"])
    description = st.text_area("Describe what you need:")
    
    if st.button("Generate Code", type="primary"):
        if description:
            model = genai.GenerativeModel('gemini-pro')
            prompt = f"Write {language} code for: {description}"
            response = model.generate_content(prompt)
            st.code(response.text, language=language.lower())

generate_code_with_gemini()

# Navigation footer
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🏠 Home"):
        st.switch_page("main.py")
with col2:
    if st.button("← Previous"):
        st.switch_page("pages/2_image_analysis.py")
with col3:
    if st.button("Next →"):
        st.switch_page("pages/4_document_summarizer.py")
