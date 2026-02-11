from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import sqlite3
import pandas as pd
import tempfile
import google.generativeai as genai

# ============================================================
# CONFIGURE GEMINI API
# ============================================================
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# ============================================================
# CUSTOM CSS FOR ENHANCED UI
# ============================================================
st.markdown("""
    <style>
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 12px;
            margin-bottom: 20px;
        }
        
        .header h1 {
            margin: 0;
            font-size: 2.2em;
            font-weight: 900;
        }
        
        .header p {
            margin: 10px 0 0 0;
            font-size: 1em;
            opacity: 0.95;
        }
        
        .success-box {
            background: #d4edda;
            border: 1px solid #28a745;
            padding: 12px;
            border-radius: 8px;
            color: #155724;
            margin: 10px 0;
        }
        
        .info-box {
            background: #d1ecf1;
            border: 1px solid #0c5460;
            padding: 12px;
            border-radius: 8px;
            color: #0c5460;
            margin: 10px 0;
        }
        
        .warning-box {
            background: #fff3cd;
            border: 1px solid #856404;
            padding: 12px;
            border-radius: 8px;
            color: #856404;
            margin: 10px 0;
        }
        
        .query-box {
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            padding: 12px;
            border-radius: 6px;
            margin: 10px 0;
            font-family: monospace;
        }
        
        .result-table {
            background: #f5f7fa;
            border-radius: 8px;
            padding: 15px;
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
    <div class="header">
        <h1>🗄️ Natural Language SQL Query Generator</h1>
        <p>Convert natural language to SQL queries - Upload custom database files or use sample data</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
**Features:**
- 📤 Upload SQL files (`.sql`, `.db`, `.sqlite`)
- 🤖 Convert natural language to SQL
- 🔍 Execute queries on your database
- 📊 View results in table format
- 💾 Download results as CSV
- 📝 Sample database included
""")

st.markdown("---")

# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================
if "db_connection" not in st.session_state:
    st.session_state.db_connection = None
if "db_path" not in st.session_state:
    st.session_state.db_path = None
if "db_name" not in st.session_state:
    st.session_state.db_name = None
if "table_schema" not in st.session_state:
    st.session_state.table_schema = None
if "query_history" not in st.session_state:
    st.session_state.query_history = []

# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def create_sample_database():
    """Create a sample SQLite database with STUDENT table"""
    temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
    db_path = temp_db.name
    temp_db.close()
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create STUDENT table
        cursor.execute("""
            CREATE TABLE STUDENT (
                ID INTEGER PRIMARY KEY,
                NAME TEXT,
                CLASS TEXT,
                SECTION TEXT,
                MARKS INTEGER
            )
        """)
        
        # Insert sample data
        sample_data = [
            (1, 'Alice', 'Machine Learning', 'A', 85),
            (2, 'Bob', 'Web Development', 'B', 90),
            (3, 'Charlie', 'Machine Learning', 'A', 78),
            (4, 'Diana', 'Data Science', 'A', 88),
            (5, 'Eve', 'Web Development', 'A', 92),
            (6, 'Frank', 'Machine Learning', 'B', 75),
            (7, 'Grace', 'Data Science', 'B', 81),
            (8, 'Henry', 'Web Development', 'B', 87),
        ]
        
        cursor.executemany(
            "INSERT INTO STUDENT VALUES (?, ?, ?, ?, ?)",
            sample_data
        )
        
        conn.commit()
        conn.close()
        
        return db_path
    except Exception as e:
        st.error(f"❌ Error creating sample database: {str(e)}")
        return None

def get_database_schema(conn):
    """Get schema information from database"""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        schema_info = {}
        for table in tables:
            table_name = table[0]
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            schema_info[table_name] = {
                "columns": [col[1] for col in columns],
                "types": [col[2] for col in columns]
            }
        
        return schema_info
    except Exception as e:
        st.error(f"❌ Error getting schema: {str(e)}")
        return None

def generate_sql_query(natural_language_query, schema_info):
    """Use Gemini to convert natural language to SQL"""
    try:
        schema_text = "Database Schema:\n"
        for table_name, info in schema_info.items():
            columns = ", ".join([f"{col} ({type_})" for col, type_ in zip(info["columns"], info["types"])])
            schema_text += f"- Table: {table_name} ({columns})\n"
        
        prompt = f"""You are an expert SQL developer. 
Convert the following natural language query to SQL.

{schema_text}

Natural Language Query: {natural_language_query}

Return ONLY the SQL query, no explanations.
Ensure the query is valid for SQLite."""
        
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(prompt)
        
        return response.text.strip()
    except Exception as e:
        st.error(f"❌ Error generating SQL: {str(e)}")
        return None

def execute_sql_query(conn, sql_query):
    """Execute SQL query and return results"""
    try:
        df = pd.read_sql_query(sql_query, conn)
        return df
    except Exception as e:
        st.error(f"❌ Error executing query: {str(e)}")
        return None

def load_sql_file(file_path):
    """Load SQL file and create database"""
    try:
        temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        db_path = temp_db.name
        temp_db.close()
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Read and execute SQL file
        with open(file_path, 'r', encoding='utf-8') as f:
            sql_content = f.read()
            
        # Execute all statements
        cursor.executescript(sql_content)
        conn.commit()
        
        return db_path, conn
    except Exception as e:
        st.error(f"❌ Error loading SQL file: {str(e)}")
        return None, None

def load_sql_dump(file_content):
    """Load SQL dump from uploaded file"""
    try:
        temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        db_path = temp_db.name
        temp_db.close()
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Decode if bytes
        if isinstance(file_content, bytes):
            sql_content = file_content.decode('utf-8')
        else:
            sql_content = file_content
        
        # Execute all statements
        cursor.executescript(sql_content)
        conn.commit()
        
        return db_path, conn
    except Exception as e:
        st.error(f"❌ Error loading SQL dump: {str(e)}")
        return None, None

# ============================================================
# MAIN APP
# ============================================================

st.subheader("📤 Database Selection")

# Tabs for different input methods
tab1, tab2, tab3 = st.tabs(["📤 Upload SQL File", "📁 Upload Database", "📊 Sample Data"])

with tab1:
    st.markdown("### Upload SQL Dump File")
    st.write("Upload a `.sql` file containing CREATE TABLE and INSERT statements")
    
    sql_file = st.file_uploader(
        "Choose SQL file",
        type=["sql", "txt"],
        key="sql_uploader"
    )
    
    if sql_file:
        col1, col2 = st.columns([2, 1])
        with col1:
            st.info(f"📄 File: {sql_file.name}")
        with col2:
            if st.button("Load SQL File", type="primary"):
                with st.spinner("Loading SQL file..."):
                    file_content = sql_file.read()
                    db_path, conn = load_sql_dump(file_content)
                    
                    if conn:
                        st.session_state.db_connection = conn
                        st.session_state.db_path = db_path
                        st.session_state.db_name = sql_file.name
                        st.session_state.table_schema = get_database_schema(conn)
                        st.success(f"✅ SQL file loaded successfully!")
                        st.rerun()

with tab2:
    st.markdown("### Upload SQLite Database File")
    st.write("Upload a `.db` or `.sqlite` database file")
    
    db_file = st.file_uploader(
        "Choose database file",
        type=["db", "sqlite", "sqlite3"],
        key="db_uploader"
    )
    
    if db_file:
        col1, col2 = st.columns([2, 1])
        with col1:
            st.info(f"💾 File: {db_file.name}")
        with col2:
            if st.button("Load Database", type="primary", key="load_db"):
                with st.spinner("Loading database..."):
                    temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
                    db_path = temp_db.name
                    temp_db.close()
                    
                    with open(db_path, 'wb') as f:
                        f.write(db_file.getbuffer())
                    
                    try:
                        conn = sqlite3.connect(db_path)
                        st.session_state.db_connection = conn
                        st.session_state.db_path = db_path
                        st.session_state.db_name = db_file.name
                        st.session_state.table_schema = get_database_schema(conn)
                        st.success(f"✅ Database loaded successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error loading database: {str(e)}")

with tab3:
    st.markdown("### Use Sample Database")
    st.write("Load a pre-built STUDENT database with sample data")
    st.info("""
    **Sample Database Contains:**
    - Table: STUDENT
    - Columns: ID, NAME, CLASS, SECTION, MARKS
    - 8 sample records
    
    **Example Queries:**
    - "Show all students"
    - "What is the average mark?"
    - "Students in ML class"
    """)
    
    if st.button("Load Sample Database", type="primary", key="load_sample"):
        with st.spinner("Creating sample database..."):
            db_path = create_sample_database()
            if db_path:
                conn = sqlite3.connect(db_path)
                st.session_state.db_connection = conn
                st.session_state.db_path = db_path
                st.session_state.db_name = "sample_database.db"
                st.session_state.table_schema = get_database_schema(conn)
                st.success("✅ Sample database loaded!")
                st.rerun()

# ============================================================
# DATABASE INFO
# ============================================================

if st.session_state.db_connection and st.session_state.table_schema:
    st.markdown("---")
    st.subheader("📊 Database Information")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Database", st.session_state.db_name or "Unknown")
    with col2:
        num_tables = len(st.session_state.table_schema)
        st.metric("Tables", num_tables)
    with col3:
        total_columns = sum(len(info["columns"]) for info in st.session_state.table_schema.values())
        st.metric("Total Columns", total_columns)
    
    # Show schema details
    with st.expander("🔍 Database Schema Details"):
        for table_name, info in st.session_state.table_schema.items():
            st.markdown(f"**Table: {table_name}**")
            schema_df = pd.DataFrame({
                "Column Name": info["columns"],
                "Data Type": info["types"]
            })
            st.dataframe(schema_df, use_container_width=True, hide_index=True)
            st.divider()

# ============================================================
# QUERY GENERATOR
# ============================================================

if st.session_state.db_connection:
    st.markdown("---")
    st.subheader("🤖 Query Generator")
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        natural_query = st.text_input(
            "Enter your query in natural language",
            placeholder="e.g., 'Show me all students with marks greater than 85'",
            key="natural_query"
        )
    
    with col2:
        generate_btn = st.button("🚀 Generate & Execute", type="primary", use_container_width=True)
    
    # Generate and execute query
    if generate_btn and natural_query:
        with st.spinner("🤔 Generating SQL query..."):
            sql_query = generate_sql_query(natural_query, st.session_state.table_schema)
            
            if sql_query:
                st.markdown("---")
                
                # Show generated SQL
                st.markdown("**Generated SQL Query:**")
                st.markdown(f"""
                    <div class="query-box">
                    {sql_query}
                    </div>
                """, unsafe_allow_html=True)
                
                # Execute query
                with st.spinner("⚡ Executing query..."):
                    results = execute_sql_query(st.session_state.db_connection, sql_query)
                    
                    if results is not None:
                        st.success(f"✅ Query executed successfully! ({len(results)} rows)")
                        
                        # Show results
                        st.markdown("**Query Results:**")
                        st.dataframe(results, use_container_width=True, hide_index=True)
                        
                        # Download CSV
                        csv = results.to_csv(index=False)
                        st.download_button(
                            label="📥 Download as CSV",
                            data=csv,
                            file_name="query_results.csv",
                            mime="text/csv"
                        )
                        
                        # Add to history
                        st.session_state.query_history.append({
                            "natural": natural_query,
                            "sql": sql_query,
                            "timestamp": pd.Timestamp.now()
                        })

# ============================================================
# QUERY HISTORY
# ============================================================

if st.session_state.query_history:
    st.markdown("---")
    st.subheader("📜 Query History")
    
    for i, query in enumerate(reversed(st.session_state.query_history[-5:]), 1):
        with st.expander(f"Query {i}: {query['natural'][:50]}..."):
            st.write(f"**Natural Language:** {query['natural']}")
            st.markdown(f"""
                <div class="query-box">
                {query['sql']}
                </div>
            """, unsafe_allow_html=True)
            st.write(f"**Time:** {query['timestamp']}")

# ============================================================
# INFO SECTION
# ============================================================

with st.expander("💡 How to Use"):
    st.markdown("""
    ## Getting Started
    
    ### 1. Load Database
    - **Upload SQL File**: Paste SQL dump with CREATE TABLE and INSERT statements
    - **Upload Database**: Upload existing `.db` or `.sqlite` file
    - **Sample Data**: Use pre-built STUDENT database
    
    ### 2. Enter Query
    - Ask in natural language
    - Examples:
      - "Show all students"
      - "Find students with marks > 80"
      - "Average marks by class"
      - "Top 5 students by marks"
    
    ### 3. Get Results
    - AI converts to SQL
    - Query runs on your database
    - Results shown in table
    - Download as CSV
    
    ### Supported File Formats
    - `.sql` - SQL dump files
    - `.txt` - Text files with SQL
    - `.db` - SQLite database files
    - `.sqlite` - SQLite database files
    - `.sqlite3` - SQLite database files
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
    if st.button("← Previous", use_container_width=True):
        st.switch_page("pages/9_ask_questions_from_pdf.py")

with col3:
    if st.button("Next →", use_container_width=True):
        st.switch_page("pages/1_text_generation.py")
