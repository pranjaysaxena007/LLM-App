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
        .invoice-header {
            background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
            color: white;
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 25px;
            box-shadow: 0 4px 15px rgba(76, 175, 80, 0.4);
        }
        
        .invoice-header h1 {
            margin: 0;
            font-size: 2.5em;
            font-weight: 900;
        }
        
        .invoice-header p {
            margin: 10px 0 0 0;
            font-size: 1.1em;
            opacity: 0.95;
        }
        
        .upload-box {
            background: #f1f8e9;
            border: 2px dashed #4CAF50;
            border-radius: 12px;
            padding: 25px;
            margin: 20px 0;
            text-align: center;
        }
        
        .response-box {
            background: #e8f5e9;
            border-left: 5px solid #4CAF50;
            padding: 20px;
            border-radius: 8px;
            margin: 15px 0;
        }
        
        .invoice-item {
            background: white;
            border-left: 4px solid #4CAF50;
            padding: 15px;
            margin: 10px 0;
            border-radius: 6px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        }
        
        .language-selector {
            background: #C8E6C9;
            padding: 15px;
            border-radius: 8px;
            margin: 15px 0;
            border: 1px solid #4CAF50;
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
    <div class="invoice-header">
        <h1>🧾 Multi-Language Invoice Extractor</h1>
        <p>Extract and analyze invoice data from images in multiple languages</p>
    </div>
""", unsafe_allow_html=True)

# ============================================================
# FUNCTIONS
# ============================================================

def get_gemini_response(input_prompt, image, system_prompt):
    """Get response from Gemini model with image"""
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content([system_prompt, image[0], input_prompt])
    return response.text

def input_image_setup(uploaded_file):
    """Setup image for Gemini API"""
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No File Uploaded")

# ============================================================
# MAIN INTERFACE
# ============================================================

st.subheader("📸 Upload Invoice Image")

st.markdown("""
    <div class="upload-box">
        <p style="font-size: 1.1em; margin-bottom: 15px;"><strong>Upload an invoice image</strong></p>
        <p style="color: #666; margin: 0;">Supported formats: JPG, JPEG, PNG | Works with invoices in any language</p>
    </div>
""", unsafe_allow_html=True)

# Create two columns
col1, col2 = st.columns([1, 1])

with col1:
    uploaded_file = st.file_uploader(
        "Choose an invoice image:",
        type=['jpg', 'jpeg', 'png', 'webp'],
        label_visibility="collapsed"
    )

with col2:
    st.write("")

# Display image preview
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="📄 Uploaded Invoice Image", use_container_width=True)

st.markdown("---")

# Query and language selection
st.subheader("🔍 Extract Information")

col1, col2 = st.columns([2, 1])

with col1:
    user_query = st.text_area(
        "What information do you want to extract?",
        placeholder="E.g., Extract all line items and total amount",
        height=80,
        label_visibility="collapsed"
    )

with col2:
    st.write("")

# Language selection
st.markdown("""
    <div class="language-selector">
        <strong>🌐 Language Support:</strong> The invoice can be in any language. Our AI will automatically detect and process it.
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# Analysis options
st.subheader("📋 Extraction Options")

extraction_type = st.selectbox(
    "What would you like to extract?",
    [
        "Full Invoice Details",
        "Line Items Only",
        "Totals & Amounts",
        "Vendor Information",
        "Custom Query"
    ]
)

# Set system prompt based on extraction type
if extraction_type == "Full Invoice Details":
    system_prompt = """
    You are an expert invoice processing system. Extract ALL information from the invoice including:
    - Vendor/Company name and details
    - Invoice number and date
    - Line items (product/service, quantity, unit price, total)
    - Subtotal, taxes, discounts, total amount
    - Payment terms
    - Customer information
    Format the output clearly and organized.
    """
elif extraction_type == "Line Items Only":
    system_prompt = """
    You are an expert invoice processor. Extract ONLY the line items from the invoice.
    For each line item provide: Product/Service name, Quantity, Unit Price, Total Price.
    Format as a clear table or list.
    """
elif extraction_type == "Totals & Amounts":
    system_prompt = """
    You are an expert invoice processor. Extract ONLY the financial totals from the invoice.
    Provide: Subtotal, Tax amount, Discounts (if any), Final Total, and Currency.
    """
elif extraction_type == "Vendor Information":
    system_prompt = """
    You are an expert invoice processor. Extract vendor/company information from the invoice.
    Provide: Company name, Address, Phone, Email, Invoice number, and Date.
    """
else:
    system_prompt = """
    You are an expert invoice processor. Process this invoice professionally.
    Extract information as requested and format it clearly.
    """

# Extract button
st.subheader("📊 Start Extraction")

if st.button("📑 Extract Invoice Data", type="primary", use_container_width=True):
    if uploaded_file is not None:
        if extraction_type != "Custom Query" or user_query:
            with st.spinner("⏳ Processing invoice..."):
                try:
                    image_data = input_image_setup(uploaded_file)
                    
                    # Use custom query if provided
                    final_query = user_query if user_query else "Please extract all information from this invoice."
                    
                    response = get_gemini_response(final_query, image_data, system_prompt)
                    
                    st.markdown("""
                        <div class="response-box">
                            <h3 style="margin-top: 0; color: #4CAF50;">✅ Extraction Results</h3>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(response)
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Copy to clipboard button
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("📋 Copy Results", type="secondary"):
                            st.success("✅ Results copied! (Use manually)")
                    with col2:
                        if st.button("💾 Save Results", type="secondary"):
                            st.success("✅ Saved! (Feature coming soon)")
                            
                except FileNotFoundError:
                    st.markdown("""
                        <div class="error-box">
                            ❌ No image uploaded yet!
                        </div>
                    """, unsafe_allow_html=True)
                except Exception as e:
                    st.markdown(f"""
                        <div class="error-box">
                            ❌ Error: {str(e)}
                        </div>
                    """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ Please enter a custom query for extraction!")
    else:
        st.warning("⚠️ Please upload an invoice image first!")

st.markdown("---")

# Info section
with st.expander("ℹ️ Supported Invoice Types", expanded=False):
    st.markdown("""
    - **Commercial Invoices:** Standard business invoices
    - **Pro Forma Invoices:** Preliminary billing documents
    - **Credit Memos:** Return or credit documents
    - **Purchase Orders:** Purchase request documents
    - **Receipts:** Simple receipt documents
    
    **Languages Supported:** English, Spanish, French, German, Chinese, Japanese, Arabic, and 50+ more!
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
        st.switch_page("pages/7_calorie_counter.py")

with col3:
    if st.button("Next Feature →", use_container_width=True):
        st.switch_page("pages/9_chat_with_pdf.py")