from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# ============================================================
# CUSTOM CSS FOR ENHANCED UI
# ============================================================
st.markdown("""
    <style>
        .calorie-header {
            background: linear-gradient(135deg, #FF6B6B 0%, #FF8E72 100%);
            color: white;
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 25px;
            box-shadow: 0 4px 15px rgba(255, 107, 107, 0.4);
        }
        
        .calorie-header h1 {
            margin: 0;
            font-size: 2.5em;
            font-weight: 900;
        }
        
        .calorie-header p {
            margin: 10px 0 0 0;
            font-size: 1.1em;
            opacity: 0.95;
        }
        
        .upload-box {
            background: #fff5f5;
            border: 2px dashed #FF6B6B;
            border-radius: 12px;
            padding: 25px;
            margin: 20px 0;
            text-align: center;
        }
        
        .response-box {
            background: #FFF3E0;
            border-left: 5px solid #FF9800;
            padding: 20px;
            border-radius: 8px;
            margin: 15px 0;
        }
        
        .food-item {
            background: white;
            border-left: 4px solid #FF6B6B;
            padding: 12px;
            margin: 8px 0;
            border-radius: 6px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        }
        
        .info-badge {
            background: #FFE0B2;
            border-radius: 8px;
            padding: 12px;
            margin: 10px 0;
            border-left: 4px solid #FF9800;
        }
        
        .image-preview {
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            margin: 15px 0;
        }
    </style>
""", unsafe_allow_html=True)

# ============================================================
# NAVIGATION
# ============================================================
if st.button("🏠 Back to Home"):
    st.switch_page("main.py")

st.markdown("---")

# ============================================================
# PAGE HEADER
# ============================================================
st.markdown("""
    <div class="calorie-header">
        <h1>🍎 Calorie Counter</h1>
        <p>Analyze food images and get detailed calorie information using AI</p>
    </div>
""", unsafe_allow_html=True)

# ============================================================
# FUNCTIONS
# ============================================================

def get_gemini_response(input_prompt, image, system_prompt):
    """Get response from Gemini model with image"""
    model = genai.GenerativeModel("gemini-2.5-flash-lite")
    response = model.generate_content([system_prompt, image[0], input_prompt])
    return response.text

def input_image_setup(uploaded_image):
    """Setup image for Gemini API"""
    if uploaded_image is not None:
        bytes_data = uploaded_image.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_image.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No File Uploaded")

# ============================================================
# MAIN INTERFACE
# ============================================================

st.subheader("📸 Upload Food Image")

st.markdown("""
    <div class="upload-box">
        <p style="font-size: 1.1em; margin-bottom: 15px;"><strong>Upload an image of your meal</strong></p>
        <p style="color: #666; margin: 0;">Supported formats: JPG, JPEG, PNG</p>
    </div>
""", unsafe_allow_html=True)

# Create two columns for upload and preview
col1, col2 = st.columns([1, 1])

with col1:
    uploaded_file = st.file_uploader(
        "Choose a food image:",
        type=['jpg', 'jpeg', 'png'],
        label_visibility="collapsed"
    )

with col2:
    st.write("")  # Spacing

# Display image preview
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="📷 Uploaded Food Image", use_container_width=True, 
             output_format="JPEG")

st.markdown("---")

# Analysis section
st.subheader("🔍 Analysis Options")

col1, col2 = st.columns([2, 1])

with col1:
    custom_prompt = st.text_area(
        "Enter custom analysis prompt (optional):",
        placeholder="E.g., Focus on the protein content...",
        height=80,
        label_visibility="collapsed"
    )

with col2:
    analysis_type = st.selectbox(
        "Analysis Type:",
        ["Total Calories", "Detailed Breakdown", "Nutritional Info"],
        label_visibility="collapsed"
    )

st.markdown("---")

# System prompt based on analysis type
if analysis_type == "Total Calories":
    system_prompt = """
    You are an expert nutritionist. Analyze the food items in the image and calculate the total calorie intake.
    Provide a detailed breakdown of each food item with estimated calories.
    Format: Present as a clear list with item name and calorie count.
    """
elif analysis_type == "Detailed Breakdown":
    system_prompt = """
    You are an expert nutritionist. Analyze the food items in this image and provide:
    1. Each food item identified
    2. Estimated portion size
    3. Calories for each item
    4. Total calories
    5. Key nutrients (protein, carbs, fats)
    """
else:
    system_prompt = """
    You are an expert nutritionist. Analyze this meal and provide:
    1. List of all food items
    2. Estimated calories
    3. Macro nutrients (protein %, carbs %, fats %)
    4. Health recommendations
    5. Nutritional value summary
    """

st.subheader("📊 Get Calorie Analysis")

# Analysis button
if st.button("🔍 Analyze Image", type="primary", use_container_width=True):
    if uploaded_file is not None:
        with st.spinner("⏳ Analyzing food image..."):
            try:
                image_data = input_image_setup(uploaded_file)
                
                # Use custom prompt if provided, otherwise use default
                final_prompt = custom_prompt if custom_prompt else "Analyze this food image and provide calorie information."
                
                response = get_gemini_response(final_prompt, image_data, system_prompt)
                
                st.markdown("""
                    <div class="response-box">
                        <h3 style="margin-top: 0; color: #FF6B6B;">📈 Analysis Results</h3>
                """, unsafe_allow_html=True)
                
                # Format response with better styling
                st.markdown(response)
                
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Add save option
                if st.button("💾 Save Results", type="secondary"):
                    st.success("✅ Results saved! (Feature coming soon)")
                    
            except FileNotFoundError:
                st.error("❌ No image uploaded yet!")
            except Exception as e:
                st.error(f"❌ Error analyzing image: {str(e)}")
    else:
        st.warning("⚠️ Please upload a food image first!")

st.markdown("---")

# Tips section
with st.expander("💡 Tips for Best Results", expanded=False):
    st.markdown("""
    - **Good lighting:** Ensure the food is well-lit for accurate analysis
    - **Clear view:** Show food items clearly without overlapping
    - **Multiple angles:** Different angles can improve accuracy
    - **Include scale:** If possible, include a reference object for size estimation
    - **Fresh photos:** Recent food images give more accurate calorie counts
    """)

st.markdown("---")

# ============================================================
# NAVIGATION FOOTER
# ============================================================
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("main.py")

with col2:
    if st.button("← Previous Feature", use_container_width=True):
        st.switch_page("pages/6_translation_tool.py")

with col3:
    if st.button("Next Feature →", use_container_width=True):
        st.switch_page("pages/8_muli_lang_invoice_extract.py")