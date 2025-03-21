from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import List, Dict, Any, Optional
from src.data.data_processor import DataProcessor
import pandas as pd
import json
import logging
import os
from tempfile import NamedTemporaryFile

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize data processor
data_processor = DataProcessor()

def validate_file_extension(filename: str, allowed_extensions: List[str]) -> bool:
    """Validate file extension"""
    return filename.lower().endswith(tuple(allowed_extensions))

def save_upload_file_tmp(upload_file: UploadFile) -> str:
    """Save uploaded file to temporary location"""
    try:
        suffix = os.path.splitext(upload_file.filename)[1]
        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            content = upload_file.file.read()
            tmp.write(content)
            return tmp.name
    except Exception as e:
        logger.error(f"Error saving temporary file: {str(e)}")
        raise

@router.post("/upload")
async def upload_data(
    file: UploadFile = File(...),
    format_type: str = Form("csv")
) -> Dict[str, Any]:
    """
    Upload and process a data file
    
    Args:
        file: The file to upload (CSV, XLSX, or JSON)
        format_type: Type of file ('csv', 'xlsx', 'json')
    """
    try:
        # Validate file extension
        allowed_extensions = ['.csv', '.xlsx', '.json']
        if not validate_file_extension(file.filename, allowed_extensions):
            raise ValueError(f"Unsupported file type. Allowed types: {', '.join(allowed_extensions)}")
        
        # Save file temporarily
        temp_file = await save_upload_file_tmp(file)
        logger.info(f"Temporary file saved: {temp_file}")
        
        try:
            # Process data based on format
            if format_type == "xlsx":
                # Convert XLSX to CSV first
                logger.info("Converting XLSX to CSV...")
                df = data_processor.import_data(temp_file, format_type="xlsx")
            elif format_type == "csv":
                df = data_processor.import_data(temp_file, format_type="csv")
            elif format_type == "json":
                df = data_processor.import_data(temp_file, format_type="json")
            else:
                raise ValueError(f"Unsupported format type: {format_type}")
            
            # Log successful processing
            logger.info(f"Successfully processed {format_type} file: {file.filename}")
            
            return {
                "message": "Data uploaded and processed successfully",
                "original_file": file.filename,
                "format_type": format_type,
                "shape": df.shape,
                "columns": df.columns.tolist(),
                "preview": df.head().to_dict(orient="records"),
                "cleaning_log": data_processor.get_cleaning_log()
            }
            
        finally:
            # Clean up temporary file
            try:
                os.unlink(temp_file)
                logger.info(f"Temporary file removed: {temp_file}")
            except Exception as e:
                logger.warning(f"Error removing temporary file: {str(e)}")
        
    except Exception as e:
        logger.error(f"Error processing upload: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/clean")
async def clean_data(cleaning_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Clean data based on provided configuration
    
    Example cleaning_config:
    {
        "missing_data": {
            "column1": "mean",
            "column2": "median"
        },
        "standardize": ["column1", "column3"],
        "normalize": ["column2"],
        "deduplicate": {
            "subset": ["column1", "column2"],
            "keep": "first"
        },
        "verification": {
            "column1": {
                "type": "numeric",
                "range": [0, 100]
            }
        }
    }
    """
    try:
        # Apply cleaning operations based on config
        if "missing_data" in cleaning_config:
            data_processor.rebuild_missing_data(cleaning_config["missing_data"])
        
        if "standardize" in cleaning_config:
            data_processor.standardize(cleaning_config["standardize"])
        
        if "normalize" in cleaning_config:
            data_processor.normalize(cleaning_config["normalize"])
        
        if "deduplicate" in cleaning_config:
            data_processor.deduplicate(**cleaning_config["deduplicate"])
        
        if "verification" in cleaning_config:
            data_processor.verify_and_enrich(cleaning_config["verification"])
        
        # Get processed data and cleaning log
        processed_data = data_processor.export_data("dict")
        cleaning_log = data_processor.get_cleaning_log()
        
        return {
            "message": "Data cleaned successfully",
            "cleaning_log": cleaning_log,
            "processed_data": processed_data
        }
        
    except Exception as e:
        logger.error(f"Error cleaning data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/merge")
async def merge_datasets(
    other_data: Dict[str, Any],
    merge_config: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Merge current dataset with another dataset
    
    Example merge_config:
    {
        "merge_on": ["column1", "column2"],
        "how": "left"
    }
    """
    try:
        # Convert other data to DataFrame
        other_df = pd.DataFrame.from_dict(other_data)
        
        # Merge datasets
        data_processor.merge_datasets(
            other_df,
            merge_on=merge_config["merge_on"],
            how=merge_config.get("how", "left")
        )
        
        # Get merged data and cleaning log
        merged_data = data_processor.export_data("dict")
        cleaning_log = data_processor.get_cleaning_log()
        
        return {
            "message": "Datasets merged successfully",
            "cleaning_log": cleaning_log,
            "merged_data": merged_data
        }
        
    except Exception as e:
        logger.error(f"Error merging datasets: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/export")
async def export_data(format_type: str = "json") -> Dict[str, Any]:
    """
    Export processed data in specified format
    """
    try:
        # Export data in requested format
        exported_data = data_processor.export_data(format_type)
        cleaning_log = data_processor.get_cleaning_log()
        
        return {
            "message": f"Data exported as {format_type}",
            "cleaning_log": cleaning_log,
            "exported_data": exported_data
        }
        
    except Exception as e:
        logger.error(f"Error exporting data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/cleaning-log")
async def get_cleaning_log() -> Dict[str, Any]:
    """
    Get the complete data cleaning operation log
    """
    try:
        cleaning_log = data_processor.get_cleaning_log()
        
        return {
            "cleaning_log": cleaning_log
        }
        
    except Exception as e:
        logger.error(f"Error retrieving cleaning log: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
async def get_available_data() -> Dict[str, List[str]]:
    """
    Get a list of available data sources and datasets
    """
    try:
        # TODO: Implement data source listing
        return {
            "data_sources": ["cassandra"],
            "available_datasets": ["financial_data", "market_data"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{dataset_name}")
async def get_dataset(dataset_name: str) -> Dict[str, Any]:
    """
    Get data from a specific dataset
    """
    try:
        # TODO: Implement dataset retrieval
        return {
            "dataset": dataset_name,
            "status": "not implemented",
            "message": "Dataset retrieval functionality coming soon"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 