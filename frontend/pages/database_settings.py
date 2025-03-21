import streamlit as st
import time
from utils.database import DatabaseManager

# Set page config
st.set_page_config(
    page_title="Database Settings - Financial Analysis System",
    page_icon="🔧",
    layout="wide"
)

# Initialize database manager
@st.cache_resource
def get_db_manager():
    return DatabaseManager()

db = get_db_manager()

# Page header
st.title("Database Settings")
st.markdown("---")

# Connection status section
st.header("Connection Status")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Current Configuration")
    st.write("Supabase URL:")
    st.write(f"- Found: {bool(db.supabase_url)}")
    if db.supabase_url:
        st.write(f"- URL: {db.supabase_url}")
    
    st.write("\nSupabase Key:")
    st.write(f"- Found: {bool(db.supabase_key)}")
    if db.supabase_key:
        st.write(f"- Length: {len(db.supabase_key)} characters")
    
    st.write("\nConnection Status:")
    st.write(f"- Client initialized: {db.client is not None}")

with col2:
    st.subheader("Connection Test")
    if st.button("Test Current Connection"):
        try:
            result = db.test_connection()
            if result:
                st.success("✅ Connection successful!")
                st.write("Connection Details:")
                st.json({
                    "url_valid": bool(db.supabase_url),
                    "key_valid": bool(db.supabase_key),
                    "connection": "active",
                    "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
                })
            else:
                st.error("❌ Connection failed!")
        except Exception as e:
            st.error(f"❌ Connection error: {str(e)}")

# Manual verification section
st.markdown("---")
st.header("Manual Credential Verification")
st.write("Use this section to verify Supabase credentials without changing the current configuration.")

test_url = st.text_input("Test Supabase URL:", type="default")
test_key = st.text_input("Test Supabase Key:", type="password")

if st.button("Verify Credentials"):
    if test_url and test_key:
        try:
            result = db.verify_credentials(test_url, test_key)
            if result:
                st.success("✅ Credentials are valid!")
            else:
                st.error("❌ Invalid credentials!")
        except Exception as e:
            st.error(f"❌ Verification error: {str(e)}")
    else:
        st.warning("⚠️ Please enter both URL and key") 