from supabase import create_client
import pandas as pd
import os
from datetime import datetime
import json
import streamlit as st
from dotenv import load_dotenv, find_dotenv
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self):
        # Load environment variables
        env_path = Path(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))) / '.env'
        if env_path.exists():
            load_dotenv(dotenv_path=env_path)
            st.write(f"Found .env at: {env_path}")
        
        # Initialize Supabase client with explicit environment variable loading
        self.supabase_url = os.getenv('SUPABASE_URL', '').strip()
        self.supabase_key = os.getenv('SUPABASE_KEY', '').strip()
        self.client = None
        
        # Try to initialize connection
        if self.supabase_url and self.supabase_key:
            try:
                self.client = create_client(self.supabase_url, self.supabase_key)
                st.success("✅ Successfully connected to Supabase!")
            except Exception as e:
                st.error(f"⚠️ Failed to connect to Supabase: {str(e)}")
        else:
            st.warning("⚠️ Supabase credentials not found. Using session storage only.")

    def test_connection(self) -> bool:
        """Test the current Supabase connection"""
        if not self.client:
            return False
        
        try:
            # Try to perform a simple query to verify connection
            result = self.client.table('file_uploads').select('id').limit(1).execute()
            return True
        except Exception as e:
            logger.error(f"Connection test failed: {str(e)}")
            return False

    def verify_credentials(self, url: str, key: str) -> bool:
        """Verify if the provided credentials are valid"""
        # First check format
        if not is_valid_supabase_url(url):
            raise ValueError("Invalid Supabase URL format")
        if not is_valid_supabase_key(key):
            raise ValueError("Invalid Supabase key format")
        
        try:
            # Try to create a temporary client
            temp_client = create_client(url.strip(), key.strip())
            # Test the connection
            result = temp_client.table('file_uploads').select('id').limit(1).execute()
            return True
        except Exception as e:
            logger.error(f"Credential verification failed: {str(e)}")
            return False

    def save_uploaded_file(self, file_data: pd.DataFrame, file_name: str, file_type: str) -> str:
        """
        Save uploaded file data to Supabase and session state
        Returns the record ID
        """
        # Create record
        record = {
            'id': len(st.session_state["uploaded_files"]),
            'file_name': file_name,
            'file_type': file_type,
            'upload_date': datetime.now().isoformat(),
            'data': file_data.to_dict()
        }
        
        # Always save to session state first
        st.session_state["uploaded_files"].append(record)
        
        # Try to save to Supabase if available
        if self.client:
            try:
                # Convert DataFrame to JSON for storage
                data_json = file_data.to_json(date_format='iso')
                
                # Create record in uploads table
                supabase_record = {
                    'file_name': file_name,
                    'file_type': file_type,
                    'upload_date': record['upload_date'],
                    'data': data_json
                }
                
                result = self.client.table('file_uploads').insert(supabase_record).execute()
                return result.data[0]['id']
            except Exception as e:
                st.warning(f"Could not save to Supabase: {str(e)}. File saved in session only.")
        
        return str(record['id'])

    def get_file_history(self) -> pd.DataFrame:
        """
        Get history of uploaded files
        Returns DataFrame with file metadata
        """
        # Try to get from Supabase first
        if self.client:
            try:
                result = self.client.table('file_uploads').select(
                    'id',
                    'file_name',
                    'file_type',
                    'upload_date'
                ).order('upload_date', desc=True).execute()
                
                return pd.DataFrame(result.data)
            except Exception as e:
                st.warning(f"Could not fetch from Supabase: {str(e)}. Using session data.")
        
        # Return session state data if no Supabase or if Supabase fails
        return pd.DataFrame([
            {
                'id': str(f['id']),
                'file_name': f['file_name'],
                'file_type': f['file_type'],
                'upload_date': f['upload_date']
            }
            for f in st.session_state["uploaded_files"]
        ])

    def get_file_data(self, file_id: str) -> pd.DataFrame:
        """
        Retrieve file data by ID
        Returns DataFrame
        """
        # Try Supabase first if available
        if self.client:
            try:
                result = self.client.table('file_uploads').select(
                    'data'
                ).eq('id', file_id).single().execute()
                
                if result.data:
                    return pd.read_json(result.data['data'])
            except Exception as e:
                st.warning(f"Could not fetch from Supabase: {str(e)}. Trying session storage.")
        
        # Try to get from session state
        try:
            file_id = int(file_id)
            file_data = next(
                (f['data'] for f in st.session_state["uploaded_files"] if f['id'] == file_id),
                None
            )
            if file_data:
                return pd.DataFrame(file_data)
        except Exception as e:
            st.error(f"Error retrieving file from session: {str(e)}")
        
        return None

    def delete_file(self, file_id: str) -> bool:
        """
        Delete file record by ID
        Returns success status
        """
        success = False
        
        # Try to delete from Supabase if available
        if self.client:
            try:
                self.client.table('file_uploads').delete().eq('id', file_id).execute()
                success = True
            except Exception as e:
                st.warning(f"Could not delete from Supabase: {str(e)}")
        
        # Always try to delete from session state
        try:
            file_id = int(file_id)
            st.session_state["uploaded_files"] = [
                f for f in st.session_state["uploaded_files"] if f['id'] != file_id
            ]
            success = True
        except Exception as e:
            st.error(f"Error deleting file from session: {str(e)}")
        
        return success

# Initialize session state
if "uploaded_files" not in st.session_state:
    st.session_state["uploaded_files"] = [] 