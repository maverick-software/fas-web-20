import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from utils.file_handler import convert_to_csv, clean_dataframe, get_excel_sheets
from utils.database import DatabaseManager
import os
import time
import io

# Clear cache to ensure we get fresh instance
st.cache_resource.clear()

# Initialize database manager
@st.cache_resource
def get_db_manager():
    return DatabaseManager()

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

# Initialize database and show connection status
db = get_db_manager()
with st.sidebar:
    if not db.client:
        st.warning("⚠️ Running in offline mode. Data will be stored in session only.")
        st.info("Configure database in Settings page to enable cloud storage.")

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
        .stProgress > div > div {
            background-color: #1E3A8A;
        }
        /* Change sidebar app text to home */
        [data-testid="stSidebarNav"] li:first-child a p {
            visibility: hidden !important;
            position: relative !important;
        }
        [data-testid="stSidebarNav"] li:first-child a p:after {
            visibility: visible !important;
            position: absolute !important;
            content: 'Home' !important;
            left: 0 !important;
            top: 0 !important;
        }
    </style>
""", unsafe_allow_html=True)

# Main title
st.title("Financial Analysis System")
st.markdown("---")

# Create tabs for upload and history
upload_tab, history_tab = st.tabs(["Upload New Data", "File History"])

with upload_tab:
    # File upload section
    st.subheader("Upload Your Data")
    uploaded_file = st.file_uploader(
        "Drag and drop your CSV or Excel file here",
        type=["csv", "xlsx"],
        help="Supported formats: CSV, XLSX"
    )

    # Create a session state for storing sheet data if it doesn't exist
    if 'sheet_files' not in st.session_state:
        st.session_state.sheet_files = None
    if 'processing_status' not in st.session_state:
        st.session_state.processing_status = None
    if 'processing_progress' not in st.session_state:
        st.session_state.processing_progress = 0.0

    # Add debug expander
    debug_expander = st.expander("Debug Information", expanded=False)
    with debug_expander:
        if 'debug_messages' not in st.session_state:
            st.session_state.debug_messages = []
        
        # Create a container for the buttons
        button_container = st.container()
        
        # Add buttons in a single column layout
        with button_container:
            # Clear debug logs button
            st.button("Clear Debug Logs", key="clear_debug_logs", on_click=lambda: st.session_state.update({"debug_messages": []}))
            
            # Download debug logs button
            if len(st.session_state.debug_messages) > 0:
                # Create CSV content
                csv_content = "Timestamp,Message\n"
                for msg in st.session_state.debug_messages:
                    timestamp = msg[1:msg.find(']')]
                    message = msg[msg.find(']')+2:]
                    message = f'"{message}"' if ',' in message else message
                    csv_content += f"{timestamp},{message}\n"
                
                st.download_button(
                    label="Download Debug Logs",
                    data=csv_content,
                    file_name=f"debug_logs_{time.strftime('%Y%m%d_%H%M%S')}.csv",
                    mime='text/csv',
                    key="download_debug_logs"
                )
        
        st.markdown("---")  # Add a separator
        
        # Display debug messages
        for msg in st.session_state.debug_messages:
            st.text(msg)

    def add_debug_message(message: str):
        """Helper function to add timestamped debug messages"""
        timestamp = time.strftime('%H:%M:%S')
        st.session_state.debug_messages.append(f"[{timestamp}] {message}")
        with debug_expander:
            st.text(f"[{timestamp}] {message}")

    if uploaded_file is not None:
        try:
            # Create progress indicators
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            def update_progress(progress: float, status: str):
                """Update progress bar and status text"""
                progress_bar.progress(progress)
                status_text.text(status)
                st.session_state.processing_progress = progress
                st.session_state.processing_status = status
                add_debug_message(status)
            
            if uploaded_file.name.endswith('.xlsx'):
                try:
                    # Get list of sheets
                    update_progress(0.1, "Reading Excel file structure...")
                    sheets = get_excel_sheets(uploaded_file)
                    add_debug_message(f"Found sheets: {', '.join(sheets)}")
                    
                    # Sheet selection
                    selected_sheet = st.selectbox(
                        "Select Sheet",
                        sheets,
                        key='sheet_selector',
                        help="Select a sheet to process"
                    )
                    
                    add_debug_message(f"Selected sheet: {selected_sheet}")
                    
                    try:
                        # Convert selected sheet to CSV
                        add_debug_message(f"Starting conversion of sheet: {selected_sheet}")
                        csv_path, csv_filename = convert_to_csv(
                            uploaded_file, 
                            uploaded_file.name, 
                            sheet_name=selected_sheet,
                            progress_callback=update_progress
                        )
                        
                        add_debug_message(f"Sheet converted successfully to: {csv_filename}")
                        
                        try:
                            # Read and display the data
                            add_debug_message("Reading converted CSV file...")
                            df = pd.read_csv(csv_path)
                            add_debug_message(f"CSV loaded successfully. Shape: {df.shape}")
                            
                            # Save to database
                            file_id = db.save_uploaded_file(
                                df,
                                uploaded_file.name,
                                'xlsx'
                            )
                            st.success(f"File uploaded and saved successfully! ID: {file_id}")
                            
                            # Display data info
                            with debug_expander:
                                st.write("DataFrame Info:")
                                buffer = io.StringIO()
                                df.info(buf=buffer)
                                st.text(buffer.getvalue())
                                
                                st.write("DataFrame Head:")
                                st.write(df.head())
                                
                                st.write("DataFrame Shape:", df.shape)
                                st.write("Column Names:", list(df.columns))
                                
                                # Add memory usage information
                                memory_usage = df.memory_usage(deep=True).sum() / 1024 / 1024  # Convert to MB
                                st.write(f"Memory Usage: {memory_usage:.2f} MB")
                            
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
                                st.dataframe(df)
                                
                                # Provide download link for converted CSV
                                with open(csv_path, 'rb') as f:
                                    st.download_button(
                                        label=f"Download {selected_sheet or 'data'} as CSV",
                                        data=f,
                                        file_name=csv_filename,
                                        mime='text/csv'
                                    )
                                
                                # Clean up temporary file
                                try:
                                    os.remove(csv_path)
                                except:
                                    pass

                            with col2:
                                st.subheader("Visualization")
                                try:
                                    # Create a sample visualization
                                    if len(df.select_dtypes(include=['float64', 'int64']).columns) > 0:
                                        numeric_col = df.select_dtypes(include=['float64', 'int64']).columns[0]
                                        fig = px.histogram(df, x=numeric_col, title=f"Distribution of {numeric_col}")
                                        st.plotly_chart(fig, use_container_width=True)
                                except Exception as e:
                                    st.error(f"Error creating visualization: {str(e)}")
                            
                        except Exception as e:
                            error_msg = f"Error reading converted CSV: {str(e)}"
                            add_debug_message(f"ERROR: {error_msg}")
                            st.error(error_msg)
                            raise
                            
                    except Exception as e:
                        error_msg = f"Error converting sheet {selected_sheet}: {str(e)}"
                        add_debug_message(f"ERROR: {error_msg}")
                        st.error(error_msg)
                        raise
                        
                except Exception as e:
                    error_msg = f"Error processing Excel file: {str(e)}"
                    add_debug_message(f"ERROR: {error_msg}")
                    st.error(error_msg)
                    with debug_expander:
                        st.error("Detailed Error Information:")
                        st.exception(e)
                    
            else:  # CSV file
                try:
                    # Read CSV directly
                    df = pd.read_csv(uploaded_file)
                    
                    # Save to database
                    file_id = db.save_uploaded_file(
                        df,
                        uploaded_file.name,
                        'csv'
                    )
                    st.success(f"File uploaded and saved successfully! ID: {file_id}")
                    
                    # Display data
                    st.dataframe(df)
                    
                except Exception as e:
                    st.error(f"Error processing CSV file: {str(e)}")
                
        except Exception as e:
            error_msg = f"Error processing file: {str(e)}"
            add_debug_message(f"ERROR: {error_msg}")
            st.error(error_msg)
            with debug_expander:
                st.error("Detailed Error Information:")
                st.exception(e)
                
        finally:
            # Clear progress bar when done
            if st.session_state.processing_progress >= 1.0:
                progress_bar.empty()

with history_tab:
    st.subheader("Previously Uploaded Files")
    
    # Get file history
    file_history = db.get_file_history()
    
    if not file_history.empty:
        # Display file history with actions
        for _, row in file_history.iterrows():
            with st.expander(f"{row['file_name']} - {row['upload_date']}"):
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.text(f"Type: {row['file_type']}")
                
                with col2:
                    if st.button("Load", key=f"load_{row['id']}"):
                        # Load file data
                        df = db.get_file_data(row['id'])
                        if df is not None:
                            st.session_state.current_data = df
                            st.success("File loaded successfully!")
                            st.dataframe(df)
                        else:
                            st.error("Error loading file data")
                
                with col3:
                    if st.button("Delete", key=f"delete_{row['id']}"):
                        if db.delete_file(row['id']):
                            st.success("File deleted successfully!")
                            st.rerun()
                        else:
                            st.error("Error deleting file")
    else:
        st.info("No files have been uploaded yet.")

# Status/feedback area
st.markdown("---")
with st.expander("System Status", expanded=False):
    if uploaded_file is None:
        st.info("System is ready. Upload a file to begin analysis.")
    elif uploaded_file.name.endswith('.xlsx'):
        st.info(f"Currently viewing sheet: {selected_sheet}")
    else:
        st.info("CSV file loaded successfully.") 