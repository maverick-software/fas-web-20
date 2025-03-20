import streamlit as st
import plotly.express as px
import pandas as pd

# Set page config for a clean, minimalist look
st.set_page_config(
    page_title="Financial Analysis System",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': 'AI-Powered Financial Data Analysis Tool'
    }
)

# Apply dark theme styling
st.markdown("""
    <style>
        .stApp {
            background-color: #121212;
            color: #FFFFFF;
        }
        .stButton>button {
            background-color: #1E3A8A;
            color: #FFFFFF;
        }
        .uploadedFile {
            background-color: #1E3A8A;
            border-radius: 5px;
            padding: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# Main title
st.title("Financial Analysis System")
st.markdown("---")

# File upload section
st.subheader("Upload Your Data")
uploaded_file = st.file_uploader(
    "Drag and drop your CSV or Excel file here",
    type=["csv", "xlsx"],
    help="Supported formats: CSV, XLSX"
)

# Command input section
st.subheader("Enter Your Command")
user_command = st.text_input(
    "Type your command (e.g., 'Filter entries below $1000')",
    placeholder="Enter your command here..."
)

# Create two columns for the table and visualization
col1, col2 = st.columns(2)

with col1:
    st.subheader("Data Table")
    if uploaded_file is not None:
        try:
            # Read the file
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            st.dataframe(df)
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")

with col2:
    st.subheader("Visualization")
    if uploaded_file is not None and 'df' in locals():
        try:
            # Create a sample visualization
            if len(df.select_dtypes(include=['float64', 'int64']).columns) > 0:
                numeric_col = df.select_dtypes(include=['float64', 'int64']).columns[0]
                fig = px.histogram(df, x=numeric_col, title=f"Distribution of {numeric_col}")
                st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Error creating visualization: {str(e)}")

# Status/feedback area
st.markdown("---")
with st.expander("System Status", expanded=False):
    st.info("System is ready. Upload a file to begin analysis.") 