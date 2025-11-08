import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai

# ============================================================
# FEATURE 1: TEXT GENERATION
# Page: pages/1_text_generation.py
# Function: gemini_text_generation()
# Description: Generate creative text using Gemini AI
# ============================================================

# Load environment variables
load_dotenv()

# Configure Gemini API
try:
    api_key = os.getenv("GOOGLE_API_KEY")
    if api_key:
        genai.configure(api_key=api_key)
    else:
        st.error("❌ GOOGLE_API_KEY not found in .env file")
        st.stop()
except Exception as e:
    st.error(f"❌ Error configuring Gemini API: {str(e)}")
    st.stop()

# ============================================================
# NAVIGATION
# ============================================================
if st.button("🏠 Back to Home"):
    st.switch_page("main.py")

st.markdown("---")

# ============================================================
# PAGE CONTENT
# ============================================================
st.title("📝 Text Generation with Gemini AI")

st.markdown("""
**Function:** `gemini_text_generation()`

Generate creative, contextual, and high-quality text for various purposes including:
- Creative writing and storytelling
- Blog post and article writing
- Email composition
- Ad copy and marketing content
- Poetry and creative content
- Social media posts
""")

st.markdown("---")

# ============================================================
# MAIN FEATURE CODE
# ============================================================

def gemini_text_generation():
    """
    Generate text using Google Gemini API.
    
    Input: User prompt or topic
    Output: AI-generated text response
    """
    st.subheader("✨ Create Your Content")
    
    # Input form
    col1, col2 = st.columns([3, 1])
    
    with col1:
        prompt = st.text_area(
            "Enter your prompt or topic:",
            placeholder="E.g., Write a funny story about a cat who...",
            height=120
        )
    
    with col2:
        st.markdown("### Settings")
        temperature = st.slider(
            "Creativity Level",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.1,
            help="Higher = more creative, Lower = more factual"
        )
        
        max_tokens = st.selectbox(
            "Response Length",
            [256, 512, 1024, 2048],
            index=2
        )
    
    # Generate button
    if st.button("🚀 Generate Text", type="primary", use_container_width=True):
        if not prompt.strip():
            st.warning("⚠️ Please enter a prompt first")
        else:
            with st.spinner("✨ Generating your content..."):
                try:
                    model = genai.GenerativeModel('gemini-pro')
                    
                    response = model.generate_content(
                        prompt,
                        generation_config={
                            'temperature': temperature,
                            'max_output_tokens': max_tokens,
                        }
                    )
                    
                    # Display result
                    st.success("✅ Generation complete!")
                    st.markdown("### 📄 Generated Content")
                    st.write(response.text)
                    
                    # Copy button
                    col1, col2 = st.columns(2)
                    with col1:
                        st.code(response.text, language="text")
                    with col2:
                        if st.button("📋 Copy to Clipboard"):
                            st.success("Copied! (manually use Ctrl+C from code box)")
                
                except Exception as e:
                    st.error(f"❌ Error generating text: {str(e)}")

# Call the function
gemini_text_generation()

# ============================================================
# NAVIGATION FOOTER
# ============================================================
st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("main.py")

with col2:
    if st.button("← Previous", use_container_width=True):
        st.switch_page("main.py")

with col3:
    if st.button("Next →", use_container_width=True):
        st.switch_page("pages/2_image_analysis.py")