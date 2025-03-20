import pandas as pd
import os
from typing import Union, Tuple, Dict, List, Callable
import tempfile
from pathlib import Path
import time
import logging
import csv
import numpy as np

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_excel_sheets(file_obj: Union[str, bytes]) -> List[str]:
    """
    Gets the list of sheet names from an Excel file.
    
    Args:
        file_obj: The uploaded Excel file object
        
    Returns:
        List[str]: List of sheet names
    """
    try:
        excel_file = pd.ExcelFile(file_obj)
        sheet_names = excel_file.sheet_names
        logger.info(f"Found {len(sheet_names)} sheets: {', '.join(sheet_names)}")
        return sheet_names
    except Exception as e:
        logger.error(f"Error reading Excel sheets: {str(e)}")
        raise Exception(f"Error reading Excel sheets: {str(e)}")

def convert_single_sheet(file, sheet_name, temp_dir, base_name, log_and_update):
    """Convert a single Excel sheet to CSV with enhanced error handling and validation"""
    try:
        log_and_update(0.4, f"Converting sheet: {sheet_name}")
        
        # Try reading with openpyxl engine first
        df = pd.read_excel(file, sheet_name=sheet_name, engine='openpyxl')
        
        # Validate DataFrame is not empty
        if df.empty:
            raise ValueError(f"Sheet '{sheet_name}' is empty")
            
        # Validate DataFrame has columns
        if len(df.columns) == 0:
            raise ValueError(f"No columns found in sheet '{sheet_name}'")
            
        # Try to detect if we need to skip rows to find the real header
        if all(str(col).startswith('Unnamed: ') for col in df.columns):
            # Try to find the first non-empty row
            for i in range(len(df)):
                if not df.iloc[i].isna().all():
                    # Re-read the Excel file with the correct header row
                    df = pd.read_excel(file, sheet_name=sheet_name, header=i, engine='openpyxl')
                    break
                    
        # If still no named columns, try reading without headers
        if all(str(col).startswith('Unnamed: ') for col in df.columns):
            df = pd.read_excel(file, sheet_name=sheet_name, header=None, engine='openpyxl')
            
        log_and_update(0.6, "Cleaning data...")
        # Clean up the DataFrame
        df = clean_dataframe(df)
        
        # Final validation
        if df.empty:
            raise ValueError(f"Sheet '{sheet_name}' contains no valid data after cleaning")
        if len(df.columns) == 0:
            raise ValueError(f"No valid columns found in sheet '{sheet_name}' after cleaning")
            
        # Save to CSV
        log_and_update(0.8, "Saving to CSV...")
        new_filename = f"{base_name}_{sheet_name}.csv"
        output_path = os.path.join(temp_dir, new_filename)
        
        # Save with UTF-8 encoding and proper quoting
        df.to_csv(
            output_path,
            index=False,
            encoding='utf-8-sig',
            quoting=csv.QUOTE_NONNUMERIC,
            escapechar='\\'
        )
        
        # Verify the CSV was written correctly
        try:
            test_df = pd.read_csv(output_path)
            if test_df.empty or len(test_df.columns) == 0:
                raise ValueError("CSV verification failed: File appears to be empty or invalid")
        except Exception as e:
            raise ValueError(f"CSV verification failed: {str(e)}")
            
        log_and_update(1.0, "Conversion complete!")
        return output_path, new_filename
        
    except Exception as e:
        raise Exception(f"Error converting sheet '{sheet_name}': {str(e)}")

def convert_to_csv(
    file_obj: Union[str, bytes], 
    filename: str, 
    sheet_name: str = None,
    progress_callback: Callable[[float, str], None] = None
) -> Union[Tuple[str, str], Dict[str, Tuple[str, str]]]:
    """
    Converts an uploaded file (Excel or CSV) to CSV format.
    For Excel files with multiple sheets, converts each sheet to a separate CSV if no sheet_name is specified.
    
    Args:
        file_obj: The uploaded file object or path
        filename: Original filename
        sheet_name: Specific sheet to convert (optional)
        progress_callback: Callback function to report progress (optional)
        
    Returns:
        If sheet_name specified: Tuple[str, str]: (Path to the converted CSV file, new filename)
        If multiple sheets: Dict[str, Tuple[str, str]]: Dictionary of sheet names to (path, filename) tuples
    """
    def log_and_update(progress: float, message: str):
        """Helper function to log and update progress"""
        logger.info(message)
        if progress_callback:
            progress_callback(progress, message)

    try:
        log_and_update(0.1, "Creating temporary directory...")
        temp_dir = tempfile.mkdtemp()
        base_name = Path(filename).stem
        
        if filename.endswith('.xlsx'):
            log_and_update(0.2, "Reading Excel file...")
            if sheet_name:
                # Single sheet conversion
                return convert_single_sheet(file_obj, sheet_name, temp_dir, base_name, log_and_update)
            else:
                # Multi-sheet conversion
                excel_file = pd.ExcelFile(file_obj)
                return convert_multiple_sheets(excel_file, temp_dir, base_name, log_and_update)
                
        elif filename.endswith('.csv'):
            return convert_csv_file(file_obj, temp_dir, base_name, log_and_update)
        else:
            raise ValueError(f"Unsupported file format: {filename}")
            
    except Exception as e:
        logger.error(f"Error in convert_to_csv: {str(e)}")
        if progress_callback:
            progress_callback(1.0, f"Error: {str(e)}")
        raise Exception(f"Error converting file to CSV: {str(e)}")

def convert_multiple_sheets(excel_file: pd.ExcelFile, temp_dir: str, base_name: str, 
                          log_and_update: Callable) -> Dict[str, Tuple[str, str]]:
    """Helper function to convert multiple sheets"""
    sheet_files = {}
    total_sheets = len(excel_file.sheet_names)
    
    for idx, sheet in enumerate(excel_file.sheet_names, 1):
        progress = 0.2 + (0.6 * (idx / total_sheets))
        log_and_update(progress, f"Converting sheet {idx}/{total_sheets}: {sheet}")
        
        try:
            output_path, new_filename = convert_single_sheet(excel_file, sheet, temp_dir, base_name, 
                        lambda p, m: log_and_update(progress + (p * 0.6 / total_sheets), m))
            sheet_files[sheet] = (output_path, new_filename)
            logger.info(f"Successfully converted sheet {sheet}")
        except Exception as e:
            logger.error(f"Error converting sheet {sheet}: {str(e)}")
            continue
    
    if not sheet_files:
        error_msg = "No valid data found in any sheet"
        logger.error(error_msg)
        raise Exception(error_msg)
    
    log_and_update(1.0, "All sheets converted!")
    return sheet_files

def convert_csv_file(file_obj: Union[str, bytes], temp_dir: str, base_name: str, 
                    log_and_update: Callable) -> Tuple[str, str]:
    """Helper function to convert CSV file"""
    try:
        log_and_update(0.3, "Reading CSV file...")
        df = pd.read_csv(file_obj)
        logger.info(f"Successfully read CSV with shape: {df.shape}")
        
        log_and_update(0.6, "Cleaning data...")
        df = clean_dataframe(df)
        logger.info(f"Cleaned CSV shape: {df.shape}")
        
        new_filename = f"{base_name}.csv"
        output_path = os.path.join(temp_dir, new_filename)
        
        log_and_update(0.8, "Saving processed CSV...")
        df.to_csv(output_path, index=False)
        logger.info(f"Successfully saved processed CSV to: {output_path}")
        
        log_and_update(1.0, "Processing complete!")
        return output_path, new_filename
        
    except Exception as e:
        logger.error(f"Error in convert_csv_file: {str(e)}")
        raise

def clean_dataframe(df):
    """Clean and prepare DataFrame for CSV conversion"""
    try:
        # Drop completely empty rows and columns
        df = df.dropna(how='all').dropna(axis=1, how='all')
        
        # Clean up column names
        df.columns = [str(col).strip() for col in df.columns]
        
        # Replace empty strings with NaN
        df = df.replace(r'^\s*$', np.nan, regex=True)
        
        # Convert object columns containing only numbers to numeric
        for col in df.select_dtypes(include=['object']).columns:
            try:
                numeric_conversion = pd.to_numeric(df[col], errors='coerce')
                if not numeric_conversion.isna().all():  # If some values converted successfully
                    df[col] = numeric_conversion
            except:
                pass
                
        # Convert remaining object columns to string
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].astype(str)
            
        return df
        
    except Exception as e:
        raise Exception(f"Error cleaning DataFrame: {str(e)}") 