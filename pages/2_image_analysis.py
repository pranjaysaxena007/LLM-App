import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# Navigation
if st.button("🏠 Back to Home"):
    st.switch_page("main.py")
    

st.markdown("---")

st.title("🖼️ Image Analysis")

def analyze_image_with_gemini():
    """Analyze images using Gemini Vision API"""
    st.subheader("Upload and Analyze Images")
    
    uploaded_file = st.file_uploader("Upload an image:", type=["jpg", "jpeg", "png", "gif"])
    
    if uploaded_file and st.button("Analyze", type="primary"):
        model = genai.GenerativeModel('gemini-2.5-flash')
        image_data = uploaded_file.read()
        response = model.generate_content([
            "Analyze this image in detail. Describe what you see.",
            {"mime_type": uploaded_file.type, "data": image_data}
        ])
        st.write(response.text)

analyze_image_with_gemini()

# Navigation footer
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🏠 Home"):
        st.switch_page("main.py")
with col2:
    if st.button("← Previous"):
        st.switch_page("pages/1_text_generation.py")
with col3:
    if st.button("Next →"):
        st.switch_page("pages/3_code_generator.py")
