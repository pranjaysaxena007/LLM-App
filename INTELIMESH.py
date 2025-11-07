import streamlit as st

st.set_page_config(page_title="Intelli Mesh", page_icon="📊", layout="wide")

# Initialize session state for shared data
if "shared_data" not in st.session_state:
    st.session_state.shared_data = None

st.title("🎯 Main Dashboard")
st.write("Click a button to navigate to different features:")

# Create button layout
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 📊 Feature 1")
    st.write("Description of feature 1")
    if st.button("Go to Feature 1", use_container_width=True, type="primary"):
        st.switch_page("pages/feature1.py")

with col2:
    st.markdown("### ⚙️ Feature 2")
    st.write("Description of feature 2")
    if st.button("Go to Feature 2", use_container_width=True, type="primary"):
        st.switch_page("pages/feature2.py")

with col3:
    st.markdown("### 📈 Feature 3")
    st.write("Description of feature 3")
    if st.button("Go to Feature 3", use_container_width=True, type="primary"):
        st.switch_page("pages/feature3.py")
