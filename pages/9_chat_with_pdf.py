from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

 
# CUSTOM CSS FOR ENHANCED UI
 
st.markdown("""
    <style>
        .pdf-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 25px;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }
        
        .pdf-header h1 {
            margin: 0;
            font-size: 2.5em;
            font-weight: 900;
        }
        
        .pdf-header p {
            margin: 10px 0 0 0;
            font-size: 1.1em;
            opacity: 0.95;
        }
        
        .upload-section {
            background: #f5f7fa;
            border: 2px dashed #667eea;
            border-radius: 12px;
            padding: 25px;
            margin: 20px 0;
            text-align: center;
        }
        
        .question-section {
            background: white;
            border: 2px solid #667eea;
            border-radius: 12px;
            padding: 20px;
            margin: 20px 0;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
        }
        
        .response-box {
            background: #e3f2fd;
            border-left: 5px solid #2196F3;
            padding: 15px;
            border-radius: 8px;
            margin: 15px 0;
        }
        
        .status-badge {
            display: inline-block;
            background: #4CAF50;
            color: white;
            padding: 8px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: 600;
        }
        
        .info-box {
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 12px;
            border-radius: 6px;
            margin: 15px 0;
            font-size: 0.95em;
        }
    </style>
""", unsafe_allow_html=True)

 
# NAVIGATION
 
if st.button("🏠 Back to Home"):
    st.switch_page("main.py")

st.markdown("---")

 
# PAGE HEADER
 
st.markdown("""
    <div class="pdf-header">
        <h1>📚 Chat with PDF</h1>
        <p>Ask questions and get instant answers from your PDF documents using Gemini AI</p>
    </div>
""", unsafe_allow_html=True)

 
# FUNCTIONS
 

def get_pdf_text(pdf_docs):
    """Extract text from PDF documents"""
    text = ""
    for pdf in pdf_docs:
        pdf_read = PdfReader(pdf)
        for page in pdf_read.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    """Split text into manageable chunks"""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks):
    """Create and save vector store from text chunks"""
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")

def get_conversational_chain():
    """Create QA chain for answering questions"""
    prompt_template = """
    Answer the question as detailed as possible from the provided context. Make sure to provide all the details.
    
    If the answer is not available in the context, then just say "Answer not available in the provided PDF".
    Don't provide any wrong answer.
    
    Context:\\n{context}\\n
    
    Question:\\n{question}\\n
    
    Answer:
    """
    
    model = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", temperature=0.3)
    prompt = PromptTemplate(template=prompt_template, input_variables=['context', 'question'])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain

def user_input(user_question):
    """Process user question and get response"""
    try:
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
        docs = new_db.similarity_search(user_question)
        
        chain = get_conversational_chain()
        response = chain({"input_documents": docs, "question": user_question}, return_only_outputs=True)
        
        st.markdown(f"""
            <div class="response-box">
                <strong>🤖 AI Response:</strong><br><br>
                {response["output_text"]}
            </div>
        """, unsafe_allow_html=True)
    except FileNotFoundError:
        st.error("❌ No PDF uploaded yet! Please upload PDF files and click 'Process' button first.")
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

 
# MAIN INTERFACE
 

# Section 1: Upload PDF Files
st.subheader("📤 Upload PDF Files")

st.markdown("""
    <div class="upload-section">
        <p style="font-size: 1.1em; margin-bottom: 15px;"><strong>Upload one or multiple PDF files</strong></p>
        <p style="color: #666; margin: 0;">Supported format: PDF files</p>
    </div>
""", unsafe_allow_html=True)

pdf_docs = st.file_uploader(
    "Choose PDF files",
    type=['pdf'],
    accept_multiple_files=True,
    label_visibility="collapsed"
)

# Show uploaded files
if pdf_docs:
    st.markdown("**📑 Uploaded Files:**")
    cols = st.columns(len(pdf_docs))
    for idx, file in enumerate(pdf_docs):
        with cols[idx]:
            st.info(f"✅ {file.name}\n\n{file.size / 1024:.1f} KB")

# Process button
if st.button("🔄 Process PDF Files", type="primary", use_container_width=True):
    if pdf_docs:
        with st.spinner("⏳ Processing PDFs... This may take a moment..."):
            try:
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                get_vector_store(text_chunks)
                
                st.markdown("""
                    <div class="response-box">
                        <span class="status-badge">✓ SUCCESS</span>
                        <p style="margin-top: 10px;"><strong>PDFs processed successfully!</strong></p>
                        <p>You can now ask questions about the uploaded PDF content below.</p>
                    </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"❌ Error processing PDFs: {str(e)}")
    else:
        st.warning("⚠️ Please upload at least one PDF file before processing.")

st.markdown("---")

# Section 2: Ask Questions
st.subheader("❓ Ask Questions")

st.markdown("""
    <div class="info-box">
        💡 <strong>Tip:</strong> Ask specific questions about the PDF content to get accurate answers.
    </div>
""", unsafe_allow_html=True)

user_question = st.text_input(
    "Enter your question:",
    placeholder="E.g., What is the main topic of this document?",
    label_visibility="collapsed"
)

if st.button("🔍 Get Answer", type="primary", use_container_width=True):
    if user_question:
        user_input(user_question)
    else:
        st.warning("⚠️ Please enter a question first.")

st.markdown("---")

 
# NAVIGATION FOOTER
 
st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("main.py")

with col2:
    if st.button("← Previous Feature", use_container_width=True):
        st.switch_page("pages/8_invoice_extractor.py")

with col3:
    if st.button("Next Feature →", use_container_width=True):
        st.switch_page("pages/10_natural_lang_sql_query.py")
