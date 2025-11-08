from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai

 
# CUSTOM CSS FOR ENHANCED UI
 
st.markdown("""
    <style>
        .text-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 25px;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }
        
        .text-header h1 {
            margin: 0;
            font-size: 2.5em;
            font-weight: 900;
        }
        
        .text-header p {
            margin: 10px 0 0 0;
            font-size: 1.1em;
            opacity: 0.95;
        }
        
        .input-section {
            background: #f5f7fa;
            border: 2px solid #667eea;
            border-radius: 12px;
            padding: 20px;
            margin: 20px 0;
        }
        
        .response-box {
            background: #e3f2fd;
            border-left: 5px solid #2196F3;
            padding: 20px;
            border-radius: 8px;
            margin: 15px 0;
        }
        
        .settings-box {
            background: #f3e5f5;
            border: 1px solid #667eea;
            padding: 15px;
            border-radius: 8px;
            margin: 15px 0;
        }
        
        .error-box {
            background: #ffebee;
            border-left: 4px solid #f44336;
            padding: 15px;
            border-radius: 6px;
            margin: 10px 0;
        }
    </style>
""", unsafe_allow_html=True)

 
# CONFIGURE GEMINI API
 
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

 
# NAVIGATION
 
if st.button("🏠 Back to Home"):
    st.switch_page("main.py")

st.markdown("---")

 
# PAGE HEADER
 
st.markdown("""
    <div class="text-header">
        <h1>📝 Text Generation</h1>
        <p>Generate creative, high-quality text using Google Gemini AI</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
**Function:** `gemini_text_generation()`

Generate creative, contextual, and high-quality text for various purposes including:
- Creative writing and storytelling
- Blog posts and articles
- Email composition
- Marketing copy and ads
- Poetry and creative content
- Social media posts
""")

st.markdown("---")

 
# MAIN FUNCTION
 

def gemini_text_generation():
    """
    Generate text using Google Gemini API.
    
    Uses: gemini-1.5-flash-latest (latest working model)
    Input: User prompt or topic
    Output: AI-generated text response
    """
    st.subheader("✨ Create Your Content")
    
    # Input form with two columns
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="input-section">', unsafe_allow_html=True)
        prompt = st.text_area(
            "Enter your prompt or topic:",
            placeholder="E.g., Write a funny story about a cat who...",
            height=120,
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="settings-box">', unsafe_allow_html=True)
        st.markdown("### ⚙️ Settings")
        
        temperature = st.slider(
            "Creativity Level",
            min_value=0.0,
            max_value=2.0,
            value=0.7,
            step=0.1,
            help="0.0=Factual, 1.0=Balanced, 2.0=Very Creative"
        )
        
        max_tokens = st.selectbox(
            "Response Length",
            [1500, 2048, 4096, 8192],
            index=2
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Generate button
    if st.button("🚀 Generate Text", type="primary", use_container_width=True):
        if not prompt.strip():
            st.warning("⚠️ Please enter a prompt first")
        else:
            with st.spinner("✨ Generating your content... (This may take a moment)"):
                try:
                    # Use the latest working model
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    
                    response = model.generate_content(
                        prompt,
                        generation_config={
                            'temperature': temperature,
                            'max_output_tokens': max_tokens,
                            'top_p': 0.95,
                            'top_k': 40,
                        }
                    )
                    
                    # Display result
                    st.markdown("""
                        <div class="response-box">
                            <h3 style="margin-top: 0; color: #667eea;">✅ Generated Content</h3>
                    """, unsafe_allow_html=True)
                    
                    if response.candidates[0].content.parts:
                            st.write(response.candidates[0].content.parts[0].text)
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Display in code box for easy copying
                    st.markdown("**📋 Copy below:**")
                    st.code(response.text, language="text")
                    
                    # Additional options
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("📋 Copy Text", type="secondary"):
                            st.success("✅ Copy the text from the code box above using Ctrl+C")
                    
                    with col2:
                        if st.button("🔄 Generate Again", type="secondary"):
                            st.rerun()
                
                except Exception as e:
                    error_msg = str(e)
                    st.markdown(f"""
                        <div class="error-box">
                            ❌ <strong>Error:</strong><br>
                            {error_msg}
                        </div>
                    """, unsafe_allow_html=True)
                    

 
# CALL THE FUNCTION
 
gemini_text_generation()

st.markdown("---")

 
# TIPS SECTION
 
with st.expander("💡 Tips for Better Results", expanded=False):
    st.markdown("""
    **Prompt Writing Tips:**
    - Be specific about what you want
    - Provide context for the AI
    - Mention the tone or style you prefer
    - Give examples if possible
    
    **Best Practices:**
    - **Low Creativity (0.0-0.5):** For factual, structured content
    - **Medium Creativity (0.5-1.0):** For balanced, general content
    - **High Creativity (1.0-2.0):** For creative, imaginative content
    
    **Example Prompts:**
    - "Write a professional email requesting a meeting"
    - "Create a funny poem about programming"
    - "Write a product description for a smartphone"
    - "Generate 5 catchy social media posts about coffee"
    """)

st.markdown("---")

 
# NAVIGATION FOOTER
 
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