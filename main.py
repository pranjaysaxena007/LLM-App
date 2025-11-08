import streamlit as st

# ============================================================
# INTELLIMESH - Main Navigation Hub (Front Page)
# This is your main.py file
# ============================================================

st.set_page_config(
    page_title="INTELLIMESH - LLM Applications",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS FOR CARD-BASED UI
# ============================================================
st.markdown("""
    <style>
        .header-container {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 40px 20px;
            border-radius: 15px;
            color: white;
            text-align: center;
            margin-bottom: 30px;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }
        .header-title {
            font-size: 3em;
            font-weight: 900;
            margin: 0;
            letter-spacing: -1px;
        }
        .header-subtitle {
            font-size: 1.3em;
            margin-top: 10px;
            opacity: 0.95;
            font-weight: 300;
        }
        
        .feature-card {
            background: white;
            border-radius: 12px;
            padding: 25px;
            margin: 15px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
            border-left: 5px solid #667eea;
            transition: all 0.3s ease;
            height: 100%;
        }
        
        .feature-card:hover {
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.15);
            transform: translateY(-5px);
            border-left-color: #764ba2;
        }
        
        .card-icon {
            font-size: 2.5em;
            margin-bottom: 15px;
        }
        
        .card-title {
            font-size: 1.4em;
            font-weight: 700;
            color: #333;
            margin: 10px 0;
        }
        
        .card-description {
            font-size: 0.95em;
            color: #666;
            line-height: 1.6;
            margin: 12px 0;
        }
        
        .card-function {
            font-size: 0.85em;
            color: #888;
            background: #f5f5f5;
            padding: 8px 12px;
            border-radius: 6px;
            margin-top: 12px;
            font-family: monospace;
            border: 1px solid #e0e0e0;
        }
        
        .divider-text {
            text-align: center;
            color: #999;
            margin: 30px 0 20px 0;
            font-weight: 500;
        }
        
        .info-box {
            background: #e3f2fd;
            border-left: 4px solid #2196F3;
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
        }
    </style>
""", unsafe_allow_html=True)

# ============================================================
# HEADER SECTION
# ============================================================
st.markdown("""
    <div class="header-container">
        <div class="header-title">🤖 INTELLIMESH</div>
        <div class="header-subtitle">AI-Powered LLM Applications Suite</div>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
Welcome to **INTELLIMESH** - Your integrated platform for AI-powered applications using Google Gemini API.
Each feature below is a separate application you can explore independently. Click any button below to navigate!
""")

# ============================================================
# INITIALIZE SESSION STATE
# ============================================================
if "uploaded_data" not in st.session_state:
    st.session_state.uploaded_data = None

if "analysis_results" not in st.session_state:
    st.session_state.analysis_results = None

# ============================================================
# DEFINE ALL FEATURES/PAGES
# ============================================================
# Format: {
#   "title": "Feature Name",
#   "icon": "emoji",
#   "description": "What this feature does",
#   "function_name": "Function that handles this",
#   "page_path": "pages/filename.py"
# }

features = [
{
"title": "Text Generation",
"icon": "📝",
"description": "Generate creative text with Gemini AI",
"function_name": "gemini_text_generation()",
"page_path": "pages/1_text_generation.py"
},
{
"title": "Image Analysis",
"icon": "🖼️",
"description": "Analyze images and extract insights",
"function_name": "analyze_image_with_gemini()",
"page_path": "pages/2_image_analysis.py"
},
{
"title": "Code Generator",
"icon": "💻",
"description": "Generate code from descriptions",
"function_name": "generate_code_with_gemini()",
"page_path": "pages/3_code_generator.py"
},
{
"title": "Document Summarizer",
"icon": "📄",
"description": "Summarize long documents",
"function_name": "summarize_document()",
"page_path": "pages/4_document_summarizer.py"
},
{
"title": "Chat Assistant",
"icon": "💬",
"description": "Interactive chat with AI",
"function_name": "chat_with_gemini()",
"page_path": "pages/5_chat_assistant.py"
},
{
"title": "Translation Tool",
"icon": "🌐",
"description": "Translate to 50+ languages",
"function_name": "translate_text()",
"page_path": "pages/6_translation_tool.py"
},
{
"title": "Calorie Counter",
"icon": "🍎",
"description": "Analyze food images and get calorie info",
"function_name": "count_calories()",
"page_path": "pages/7_calorie_counter.py"
},
{
"title": "Invoice Extractor",
"icon": "🧾",
"description": "Extract data from multi-language invoices",
"function_name": "extract_invoice_data()",
"page_path": "pages/8_muli_lang_invoice_extract.py"
},
{
"title": "Chat with PDF",
"icon": "📚",
"description": "Ask questions from PDF documents using RAG",
"function_name": "chat_with_pdf()",
"page_path": "pages/9_chat_with_pdf.py"
},

{
"title": "SQL Query Generator",
"icon": "🔍",
"description": "Convert natural language to SQL queries",
"function_name": "natural_language_sql()",
"page_path": "pages/10_natural_lang_sql_query.py"
}
]

# ============================================================
# DISPLAY FEATURES AS CARDS WITH NAVIGATION BUTTONS
# ============================================================
st.markdown('<div class="divider-text">🚀 Available Features</div>', unsafe_allow_html=True)

# Create 2-column layout for cards
col1, col2 = st.columns(2)

for idx, feature in enumerate(features):
    # Alternate between col1 and col2
    current_col = col1 if idx % 2 == 0 else col2
    
    with current_col:
        st.markdown(f"""
            <div class="feature-card">
                <div class="card-icon">{feature['icon']}</div>
                <div class="card-title">{feature['title']}</div>
                <div class="card-description">{feature['description']}</div>
                <div class="card-function">Function: {feature['function_name']}</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Navigation button
        if st.button(
            f"🔗 Open {feature['title']}",
            key=f"btn_{feature['page_path']}",
            use_container_width=True,
            type="primary"
        ):
            st.switch_page(feature['page_path'])

# ============================================================
# INFO SECTION
# ============================================================
st.markdown('<div class="divider-text">ℹ️ About This Application</div>', unsafe_allow_html=True)

st.markdown("""
    <div class="info-box">
        <strong>💡 How to Use:</strong>
        <ul>
            <li>Click any "Open" button above to access that feature</li>
            <li>Each feature is a standalone application with its own interface</li>
            <li>All features use Google Gemini API for AI capabilities</li>
            <li>Your API key must be set in the .env file as GOOGLE_API_KEY</li>
        </ul>
    </div>
""", unsafe_allow_html=True)

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("""
        <div style="text-align: center;">
            <p style="color: #666; margin: 0;">🔐 INTELLIMESH v1.0 | Powered by Google Gemini API</p>
            <p style="color: #999; font-size: 0.9em; margin: 5px 0;">© 2025 | Built with Streamlit</p>
        </div>
    """, unsafe_allow_html=True)