from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import json
from datetime import datetime
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, AIMessage

 
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

 
# CUSTOM CSS FOR ENHANCED UI
 
st.markdown("""
    <style>
        .chat-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 25px;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }
        
        .chat-header h1 {
            margin: 0;
            font-size: 2.5em;
            font-weight: 900;
        }
        
        .chat-header p {
            margin: 10px 0 0 0;
            font-size: 1.1em;
            opacity: 0.95;
        }
        
        .message-user {
            background: #e3f2fd;
            border-left: 5px solid #2196F3;
            padding: 15px;
            border-radius: 8px;
            margin: 10px 0;
        }
        
        .message-ai {
            background: #f3e5f5;
            border-left: 5px solid #9c27b0;
            padding: 15px;
            border-radius: 8px;
            margin: 10px 0;
        }
        
        .chat-input-box {
            background: #f5f7fa;
            border: 2px solid #667eea;
            border-radius: 12px;
            padding: 20px;
            margin: 20px 0;
        }
        
        .context-info {
            background: #fff3e0;
            border: 1px solid #ff9800;
            padding: 10px;
            border-radius: 6px;
            font-size: 0.9em;
            margin: 10px 0;
        }
    </style>
""", unsafe_allow_html=True)

 
# DEFINE KEYS
 
HISTORY_FILE = "chat_history.json"
SESSION_KEY = "chat_messages"
STATS_KEY = "chat_stats"


# NAVIGATION
 
if st.button("🏠 Back to Home"):
    st.switch_page("main.py")

st.markdown("---")

 
# PAGE HEADER
 
st.markdown("""
    <div class="chat-header">
        <h1>💬 Chat Assistant</h1>
        <p>Interactive conversation with Gemini AI - Remembers & Uses Chat History</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
**Features:**
- 📝 Saves all conversations to JSON file
- 🧠 Uses conversation history as context for future answers
- 💾 Persistent memory across sessions
- 📊 View statistics
- 🔄 Clear history anytime
""")

st.markdown("---")

# CONVERSATION HISTORY MANAGEMENT

def load_conversation_history():
    """Load conversation history from JSON file"""
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("messages", []), data.get("stats", {})
    except Exception as e:
        st.warning(f"⚠️ Could not load history: {str(e)}")
    return [], {}

def save_conversation_history(messages, stats):
    """Save conversation history to JSON file"""
    try:
        data = {
            "messages": messages,
            "stats": stats,
            "last_updated": datetime.now().isoformat()
        }
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        st.error(f"❌ Error saving history: {str(e)}")
        return False

def add_message_to_history(messages, role, content):
    """Add a new message to history"""
    message_obj = {
        "role": role,
        "content": content,
        "timestamp": datetime.now().isoformat()
    }
    messages.append(message_obj)
    return messages

def update_statistics(stats, role):
    """Update conversation statistics"""
    if "total_messages" not in stats:
        stats["total_messages"] = 0
        stats["user_messages"] = 0
        stats["ai_messages"] = 0
        stats["conversation_start"] = datetime.now().isoformat()
    
    stats["total_messages"] += 1
    if role == "user":
        stats["user_messages"] += 1
    else:
        stats["ai_messages"] += 1
    
    stats["last_updated"] = datetime.now().isoformat()
    return stats

# ✅ CONVERT HISTORY TO LANGCHAIN FORMAT


def convert_history_to_langchain_messages(messages_data, limit=20):
    """
    Convert saved message history to LangChain message format
    
    Args:
        messages_data (list): List of message dicts from JSON
        limit (int): Limit number of previous messages to use (for context window)
    
    Returns:
        list: List of HumanMessage and AIMessage objects
    """
    langchain_messages = []
    
    # Only use last N messages for context (to avoid token limit)
    recent_messages = messages_data[-limit:] if len(messages_data) > limit else messages_data
    
    for msg in recent_messages:
        if msg["role"] == "user":
            langchain_messages.append(HumanMessage(content=msg["content"]))
        else:
            langchain_messages.append(AIMessage(content=msg["content"]))
    
    return langchain_messages

# INITIALIZE SESSION STATE

if SESSION_KEY not in st.session_state:
    loaded_messages, loaded_stats = load_conversation_history()
    st.session_state[SESSION_KEY] = loaded_messages
    st.session_state[STATS_KEY] = loaded_stats

# MAIN CHAT FUNCTION WITH MEMORY


def chat_with_memory():
    """
    Interactive chat with Gemini AI that uses conversation history as context.
    
    Key Feature: ✅ Passes entire conversation history to AI for contextual responses
    """
    
    # Sidebar controls
    with st.sidebar:
        st.markdown("### 📋 Chat Controls")
        
        # Safe stats display
        if STATS_KEY in st.session_state and st.session_state[STATS_KEY]:
            st.markdown("**📊 Conversation Stats:**")
            stats = st.session_state[STATS_KEY]
            # ✅ FIXED: Changed from st.columns(2) to st.columns(3)
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total", stats.get("total_messages", 0))
            with col2:
                st.metric("User", stats.get("user_messages", 0))
            with col3:
                st.metric("AI", stats.get("ai_messages", 0))
            st.markdown("---")
        
        # Export button
        if st.button("💾 Export Chat History", type="secondary"):
            if SESSION_KEY in st.session_state and st.session_state[SESSION_KEY]:
                export_data = {
                    "messages": st.session_state[SESSION_KEY],
                    "stats": st.session_state[STATS_KEY],
                    "exported_at": datetime.now().isoformat()
                }
                st.json(export_data)
                st.success("✅ Chat history exported")
            else:
                st.info("ℹ️ No chat history to export")
        
        # Clear button
        if st.button("🔄 Clear History", type="secondary"):
            st.session_state[SESSION_KEY] = []
            st.session_state[STATS_KEY] = {}
            if os.path.exists(HISTORY_FILE):
                os.remove(HISTORY_FILE)
            st.success("✅ Chat history cleared")
            st.rerun()
        
        st.markdown("---")
        
        # Context info
        st.info("""
        🧠 **How Memory Works:**
        - AI reads all previous messages
        - Uses them as context
        - Gives contextual responses
        - Remembers conversation
        """)
    
    # Main chat area
    st.subheader("💬 Conversation with Memory")
    
    # Display chat history
    messages_container = st.container()
    
    with messages_container:
        messages = st.session_state.get(SESSION_KEY, [])
        
        if messages:
            for msg in messages:
                if msg["role"] == "user":
                    st.markdown(f"""
                        <div class="message-user">
                            <strong>👤 You:</strong><br>
                            {msg['content']}
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                        <div class="message-ai">
                            <strong>🤖 Assistant:</strong><br>
                            {msg['content']}
                        </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("💡 Start a conversation. AI will remember everything!")
    
    st.markdown("---")
    
    # Input section
    st.subheader("✍️ Send Message")
    
    st.markdown('<div class="chat-input-box">', unsafe_allow_html=True)
    
    # ✅ FIXED: Changed from st.columns(2) for proper layout
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_input = st.text_input(
            "Type your message:",
            placeholder="Ask me anything! I'll try to answer it",
            label_visibility="collapsed",
            key="chat_input"
        )
    
    with col2:
        send_button = st.button("📤 Send", type="primary", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Process message
    if send_button and user_input.strip():
        # Safe session state access
        messages = st.session_state.get(SESSION_KEY, [])
        stats = st.session_state.get(STATS_KEY, {})
        
        # Add user message to history
        messages = add_message_to_history(messages, "user", user_input)
        stats = update_statistics(stats, "user")
        
        # Show user message
        st.markdown(f"""
            <div class="message-user">
                <strong>👤 You:</strong><br>
                {user_input}
            </div>
        """, unsafe_allow_html=True)
        
        # Generate AI response
        with st.spinner("🤔 AI is thinking (reading conversation history)..."):
            try:
                # ✅ CRITICAL: Convert history to LangChain format
                langchain_messages = convert_history_to_langchain_messages(messages, limit=20)
                
                # Show context being used
                if len(messages) > 1:
                    st.markdown("""
                        <div class="context-info">
                            🧠 Using conversation history as context (last messages)
                        </div>
                    """, unsafe_allow_html=True)
                
                # Initialize model
                model = ChatGoogleGenerativeAI(
                    model="gemini-2.5-flash",
                    temperature=0.7,
                    max_output_tokens=1024
                )
                
                # ✅ KEY: Invoke with FULL conversation history
                response = model.invoke(langchain_messages)
                
                ai_response = response.content
                
                # Add AI response to history
                messages = add_message_to_history(messages, "assistant", ai_response)
                stats = update_statistics(stats, "assistant")
                
                # Update session state
                st.session_state[SESSION_KEY] = messages
                st.session_state[STATS_KEY] = stats
                
                # Save to file
                save_conversation_history(messages, stats)
                
                # Display AI response
                st.markdown(f"""
                    <div class="message-ai">
                        <strong>🤖 Assistant:</strong><br>
                        {ai_response}
                    </div>
                """, unsafe_allow_html=True)
                
                st.success("✅ Response generated and history updated")
                
                # Rerun to show updated history
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("""
                **Troubleshooting:**
                - Check API key validity
                - Verify internet connection
                - Check API quota
                """)
    
    # Display context statistics
    messages = st.session_state.get(SESSION_KEY, [])
    stats = st.session_state.get(STATS_KEY, {})
    
    if messages:
        st.markdown("---")
        
        # ✅ FIXED: Proper column layout for statistics
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("**📈 Session Statistics:**")
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("Total", stats.get("total_messages", 0))
            with col_b:
                st.metric("Your Msgs", stats.get("user_messages", 0))
            with col_c:
                st.metric("AI Msgs", stats.get("ai_messages", 0))
        
        with col2:
            st.markdown("**📝 Context Info:**")
            if len(messages) > 1:
                st.info(f"🧠 Using {len(messages)} msgs")
            else:
                st.info("💬 Fresh chat")

# CALL THE FUNCTION

chat_with_memory()

st.markdown("---")

# INFO SECTION

with st.expander("💡 How Memory Works", expanded=False):
    st.markdown("""
    ## 🧠 Memory System
    
    **How it works:**
    1. User sends message
    2. AI reads entire conversation history
    3. AI understands context
    4. AI generates contextual response
    5. Response saved to history
    
    **Benefits:**
    - ✅ Coherent conversations
    - ✅ References previous topics
    - ✅ Remembers preferences
    - ✅ Multi-turn support
    - ✅ Persistent across sessions
    """)

st.markdown("---")

# NAVIGATION FOOTER

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("main.py")

with col2:
    if st.button("← Previous", use_container_width=True):
        st.switch_page("pages/4_document_summarizer.py")

with col3:
    if st.button("Next →", use_container_width=True):
        st.switch_page("pages/6_translation_tool.py")
