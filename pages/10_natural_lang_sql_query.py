from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import sqlite3
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# ============================================================
# CUSTOM CSS FOR ENHANCED UI
# ============================================================
st.markdown("""
    <style>
        .sql-header {
            background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%);
            color: white;
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 25px;
            box-shadow: 0 4px 15px rgba(33, 150, 243, 0.4);
        }
        
        .sql-header h1 {
            margin: 0;
            font-size: 2.5em;
            font-weight: 900;
        }
        
        .sql-header p {
            margin: 10px 0 0 0;
            font-size: 1.1em;
            opacity: 0.95;
        }
        
        .query-box {
            background: #E3F2FD;
            border: 2px solid #2196F3;
            border-radius: 12px;
            padding: 20px;
            margin: 20px 0;
        }
        
        .response-box {
            background: #E1F5FE;
            border-left: 5px solid #2196F3;
            padding: 20px;
            border-radius: 8px;
            margin: 15px 0;
        }
        
        .sql-code {
            background: #263238;
            color: #AEDD6E;
            padding: 15px;
            border-radius: 8px;
            margin: 15px 0;
            font-family: monospace;
            font-size: 0.95em;
            overflow-x: auto;
        }
        
        .result-table {
            background: white;
            border-radius: 8px;
            padding: 15px;
            margin: 15px 0;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        }
        
        .database-info {
            background: #C8E6C9;
            border: 1px solid #4CAF50;
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
            color: #c62828;
        }
        
        .success-box {
            background: #c8e6c9;
            border-left: 4px solid #4CAF50;
            padding: 15px;
            border-radius: 6px;
            margin: 10px 0;
            color: #2e7d32;
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
    <div class="sql-header">
        <h1>🔍 Natural Language SQL Query Generator</h1>
        <p>Convert natural language to SQL queries and retrieve database results instantly</p>
    </div>
""", unsafe_allow_html=True)

# ============================================================
# FUNCTIONS
# ============================================================

def get_gemini_response(question, prompt):
    """Generate SQL query from natural language using Gemini"""
    model = genai.GenerativeModel(model_name="gemini-2.5-pro")
    response = model.generate_content([prompt[0], question])
    return response.text

def read_sql_query(sql, db):
    """Execute SQL query and return results"""
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        conn.commit()
        conn.close()
        return rows
    except Exception as e:
        raise Exception(f"Database Error: {str(e)}")

# System prompt for Gemini
prompt = [
    """
    You are an expert SQL developer. Your task is to convert English questions into SQL queries.
    
    Database Schema:
    - Table: STUDENT
    - Columns: ID (Integer), NAME (Text), CLASS (Text), SECTION (Text), MARKS (Integer)
    
    Example conversions:
    1. "How many students are in the database?" → SELECT COUNT(*) FROM STUDENT;
    2. "Show all students in Machine Learning class" → SELECT * FROM STUDENT WHERE CLASS = 'Machine Learning';
    3. "What is the highest score?" → SELECT MAX(MARKS) FROM STUDENT;
    4. "List students sorted by marks" → SELECT * FROM STUDENT ORDER BY MARKS DESC;
    
    IMPORTANT RULES:
    - Return ONLY the SQL query, nothing else
    - Do NOT include backticks (`) or "SQL" label
    - Ensure the query is valid and executable
    - Use proper SQL syntax
    """
]

# ============================================================
# MAIN INTERFACE
# ============================================================

st.subheader("📝 Ask a Question")

st.markdown("""
    <div class="database-info">
        <strong>📊 Database: STUDENT</strong><br>
        <strong>Columns:</strong> ID, NAME, CLASS, SECTION, MARKS<br>
        <strong>Example:</strong> "Show all students in Python class" or "What's the average marks?"
    </div>
""", unsafe_allow_html=True)

# Question input
user_question = st.text_area(
    "Enter your question in natural language:",
    placeholder="E.g., Show all students in Data Science class with marks above 80",
    height=100,
    label_visibility="collapsed"
)

st.markdown("---")

# Query options
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🔧 Query Options")
    
with col2:
    db_file = st.selectbox(
        "Select Database:",
        ["student.db"],
        label_visibility="collapsed"
    )

st.markdown("---")

# Execute button
if st.button("⚡ Convert & Execute Query", type="primary", use_container_width=True):
    if user_question.strip():
        with st.spinner("⏳ Converting to SQL..."):
            try:
                # Generate SQL query
                sql_response = get_gemini_response(user_question, prompt)
                
                # Clean response
                sql_query = sql_response.strip()
                if sql_query.startswith("```"):
                    sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
                
                # Display generated SQL
                st.markdown("<strong>🔨 Generated SQL Query:</strong>", unsafe_allow_html=True)
                st.markdown(f"""
                    <div class="sql-code">
                    {sql_query}
                    </div>
                """, unsafe_allow_html=True)
                
                # Execute query
                with st.spinner("⏳ Executing query..."):
                    try:
                        results = read_sql_query(sql_query, db_file)
                        
                        if results:
                            st.markdown("""
                                <div class="success-box">
                                    ✅ Query executed successfully!
                                </div>
                            """, unsafe_allow_html=True)
                            
                            st.markdown("<strong>📊 Query Results:</strong>", unsafe_allow_html=True)
                            
                            st.markdown('<div class="result-table">', unsafe_allow_html=True)
                            
                            # Create table
                            if isinstance(results[0], (list, tuple)):
                                # Display as formatted table
                                col_count = len(results[0])
                                
                                # Header
                                header_cols = st.columns(col_count)
                                for idx, header in enumerate(["ID", "NAME", "CLASS", "SECTION", "MARKS"][:col_count]):
                                    with header_cols[idx]:
                                        st.markdown(f"**{header}**")
                                
                                st.markdown("---")
                                
                                # Data rows
                                for row in results:
                                    cols = st.columns(col_count)
                                    for idx, value in enumerate(row):
                                        with cols[idx]:
                                            st.write(str(value))
                                    st.markdown("---")
                            
                            st.markdown('</div>', unsafe_allow_html=True)
                            
                            # Result statistics
                            col1, col2 = st.columns(2)
                            with col1:
                                st.metric("Records Found", len(results))
                            with col2:
                                st.metric("Columns", len(results[0]) if results else 0)
                            
                            # Export option
                            if st.button("💾 Save Results", type="secondary"):
                                st.success("✅ Results saved! (Feature coming soon)")
                        else:
                            st.markdown("""
                                <div class="success-box">
                                    ✅ Query executed but no results found.
                                </div>
                            """, unsafe_allow_html=True)
                            
                    except Exception as e:
                        st.markdown(f"""
                            <div class="error-box">
                                ❌ Execution Error: {str(e)}
                            </div>
                        """, unsafe_allow_html=True)
                        
            except Exception as e:
                st.markdown(f"""
                    <div class="error-box">
                        ❌ Error converting query: {str(e)}
                    </div>
                """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Please enter a question first!")

st.markdown("---")

# Example queries
with st.expander("📖 Example Queries", expanded=False):
    st.markdown("""
    Try these natural language questions:
    
    - "How many students are there?"
    - "Show all students in Data Science class"
    - "What is the average marks of all students?"
    - "Find the student with highest marks"
    - "List students sorted by marks in descending order"
    - "How many students are in section A?"
    - "Show students with marks above 80"
    - "Get all unique classes"
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
        st.switch_page("pages/9_ask_pdf.py")

with col3:
    if st.button("Next Feature →", use_container_width=True):
        st.switch_page("main.py")