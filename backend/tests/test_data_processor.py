import pytest
import pandas as pd
import os
from src.data.data_processor import DataProcessor
from tempfile import NamedTemporaryFile

@pytest.fixture
def data_processor():
    return DataProcessor()

@pytest.fixture
def sample_xlsx_file():
    # Create a temporary XLSX file
    df = pd.DataFrame({
        'A': [1, 2, 3],
        'B': ['a', 'b', 'c'],
        'C': [1.1, 2.2, 3.3]
    })
    
    with NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
        df.to_excel(tmp.name, index=False)
        return tmp.name

def test_xlsx_to_csv_conversion(data_processor, sample_xlsx_file):
    try:
        # Convert XLSX to CSV
        csv_path = data_processor.convert_xlsx_to_csv(sample_xlsx_file)
        
        # Verify CSV file exists
        assert os.path.exists(csv_path)
        
        # Read and verify CSV contents
        df = pd.read_csv(csv_path)
        assert df.shape == (3, 3)
        assert list(df.columns) == ['A', 'B', 'C']
        assert df['A'].tolist() == [1, 2, 3]
        assert df['B'].tolist() == ['a', 'b', 'c']
        assert df['C'].tolist() == [1.1, 2.2, 3.3]
        
        # Check cleaning log
        cleaning_log = data_processor.get_cleaning_log()
        assert len(cleaning_log) == 1
        assert cleaning_log[0]['operation'] == 'convert_xlsx_to_csv'
        assert cleaning_log[0]['details']['rows'] == 3
        assert cleaning_log[0]['details']['columns'] == 3
        
    finally:
        # Clean up test files
        try:
            os.unlink(sample_xlsx_file)
            os.unlink(csv_path)
        except:
            pass

def test_import_xlsx_data(data_processor, sample_xlsx_file):
    try:
        # Import XLSX data
        df = data_processor.import_data(sample_xlsx_file, format_type='xlsx')
        
        # Verify imported data
        assert df.shape == (3, 3)
        assert list(df.columns) == ['A', 'B', 'C']
        assert df['A'].tolist() == [1, 2, 3]
        assert df['B'].tolist() == ['a', 'b', 'c']
        assert df['C'].tolist() == [1.1, 2.2, 3.3]
        
        # Check cleaning log
        cleaning_log = data_processor.get_cleaning_log()
        assert len(cleaning_log) == 2  # convert_xlsx_to_csv + import_data
        assert cleaning_log[0]['operation'] == 'convert_xlsx_to_csv'
        assert cleaning_log[1]['operation'] == 'import_data'
        
    finally:
        # Clean up test file
        try:
            os.unlink(sample_xlsx_file)
        except:
            pass

def test_invalid_xlsx_file(data_processor):
    with pytest.raises(Exception):
        data_processor.convert_xlsx_to_csv('nonexistent.xlsx') 