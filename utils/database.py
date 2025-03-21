from supabase import create_client
import pandas as pd
import os
from datetime import datetime
import json

class DatabaseManager:
    def __init__(self):
        # Initialize Supabase client
        self.supabase_url = os.getenv('SUPABASE_URL')
        self.supabase_key = os.getenv('SUPABASE_KEY')
        if not self.supabase_url or not self.supabase_key:
            raise ValueError("Supabase credentials not found in environment variables")
        self.client = create_client(self.supabase_url, self.supabase_key)

    def save_uploaded_file(self, file_data: pd.DataFrame, file_name: str, file_type: str) -> str:
        """
        Save uploaded file data to Supabase
        Returns the record ID
        """
        # Convert DataFrame to JSON for storage
        data_json = file_data.to_json(date_format='iso')
        
        # Create record in uploads table
        record = {
            'file_name': file_name,
            'file_type': file_type,
            'upload_date': datetime.now().isoformat(),
            'data': data_json
        }
        
        result = self.client.table('file_uploads').insert(record).execute()
        return result.data[0]['id']

    def get_file_history(self) -> pd.DataFrame:
        """
        Get history of uploaded files
        Returns DataFrame with file metadata
        """
        result = self.client.table('file_uploads').select(
            'id',
            'file_name',
            'file_type',
            'upload_date'
        ).order('upload_date', desc=True).execute()
        
        return pd.DataFrame(result.data)

    def get_file_data(self, file_id: str) -> pd.DataFrame:
        """
        Retrieve file data by ID
        Returns DataFrame
        """
        result = self.client.table('file_uploads').select(
            'data'
        ).eq('id', file_id).single().execute()
        
        if result.data:
            return pd.read_json(result.data['data'])
        return None

    def delete_file(self, file_id: str) -> bool:
        """
        Delete file record by ID
        Returns success status
        """
        try:
            self.client.table('file_uploads').delete().eq('id', file_id).execute()
            return True
        except Exception:
            return False 