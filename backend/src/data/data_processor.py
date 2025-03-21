import pandas as pd
import numpy as np
from typing import Dict, List, Union, Optional
from datetime import datetime
import logging
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import json
import os

logger = logging.getLogger(__name__)

class DataProcessor:
    """
    Comprehensive data processing pipeline for cleaning and preparing datasets
    """
    
    def __init__(self):
        self.cleaning_log = []
        self.original_data = None
        self.processed_data = None
        self._scaler = None
    
    def log_operation(self, operation: str, details: Dict):
        """Log a data processing operation"""
        self.cleaning_log.append({
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "details": details
        })
    
    def convert_xlsx_to_csv(self, xlsx_path: str) -> str:
        """
        Convert XLSX file to CSV format
        
        Args:
            xlsx_path: Path to the XLSX file
            
        Returns:
            Path to the generated CSV file
        """
        try:
            # Get directory and filename without extension
            directory = os.path.dirname(xlsx_path)
            base_name = os.path.splitext(os.path.basename(xlsx_path))[0]
            
            # Read XLSX file
            df = pd.read_excel(xlsx_path, engine='openpyxl')
            
            # Generate CSV path
            csv_path = os.path.join(directory, f"{base_name}.csv")
            
            # Save as CSV
            df.to_csv(csv_path, index=False)
            
            self.log_operation("convert_xlsx_to_csv", {
                "input_file": xlsx_path,
                "output_file": csv_path,
                "rows": df.shape[0],
                "columns": df.shape[1]
            })
            
            return csv_path
            
        except Exception as e:
            logger.error(f"Error converting XLSX to CSV: {str(e)}")
            raise
    
    def import_data(self, data: Union[pd.DataFrame, str, Dict], format_type: str = "dataframe") -> pd.DataFrame:
        """
        Import data from various sources
        
        Args:
            data: Input data (DataFrame, file path, or dictionary)
            format_type: Type of input ('dataframe', 'csv', 'json', 'dict', 'xlsx')
        """
        try:
            if format_type == "dataframe" and isinstance(data, pd.DataFrame):
                df = data.copy()
            elif format_type == "xlsx" and isinstance(data, str):
                # Convert XLSX to CSV first
                csv_path = self.convert_xlsx_to_csv(data)
                df = pd.read_csv(csv_path)
            elif format_type == "csv" and isinstance(data, str):
                df = pd.read_csv(data)
            elif format_type == "json" and isinstance(data, str):
                df = pd.read_json(data)
            elif format_type == "dict" and isinstance(data, dict):
                df = pd.DataFrame.from_dict(data)
            else:
                raise ValueError(f"Unsupported format type: {format_type}")
            
            self.original_data = df.copy()
            self.processed_data = df.copy()
            
            self.log_operation("import_data", {
                "format_type": format_type,
                "shape": df.shape,
                "columns": df.columns.tolist()
            })
            
            return df
            
        except Exception as e:
            logger.error(f"Error importing data: {str(e)}")
            raise
    
    def merge_datasets(self, other_data: pd.DataFrame, merge_on: Union[str, List[str]], 
                      how: str = "left") -> pd.DataFrame:
        """
        Merge current dataset with another dataset
        
        Args:
            other_data: DataFrame to merge with
            merge_on: Column(s) to merge on
            how: Type of merge ('left', 'right', 'inner', 'outer')
        """
        try:
            if self.processed_data is None:
                raise ValueError("No data loaded. Import data first.")
                
            merged_df = pd.merge(self.processed_data, other_data, on=merge_on, how=how)
            self.processed_data = merged_df
            
            self.log_operation("merge_datasets", {
                "merge_columns": merge_on,
                "merge_type": how,
                "resulting_shape": merged_df.shape
            })
            
            return merged_df
            
        except Exception as e:
            logger.error(f"Error merging datasets: {str(e)}")
            raise
    
    def rebuild_missing_data(self, methods: Dict[str, str]) -> pd.DataFrame:
        """
        Rebuild missing data using specified methods
        
        Args:
            methods: Dictionary mapping column names to imputation methods
                    ('mean', 'median', 'mode', 'forward_fill', 'backward_fill')
        """
        try:
            if self.processed_data is None:
                raise ValueError("No data loaded. Import data first.")
                
            df = self.processed_data.copy()
            
            for column, method in methods.items():
                if column not in df.columns:
                    logger.warning(f"Column {column} not found in dataset")
                    continue
                    
                if method == "mean":
                    df[column] = df[column].fillna(df[column].mean())
                elif method == "median":
                    df[column] = df[column].fillna(df[column].median())
                elif method == "mode":
                    df[column] = df[column].fillna(df[column].mode()[0])
                elif method == "forward_fill":
                    df[column] = df[column].fillna(method='ffill')
                elif method == "backward_fill":
                    df[column] = df[column].fillna(method='bfill')
                else:
                    logger.warning(f"Unsupported imputation method: {method}")
            
            self.processed_data = df
            
            self.log_operation("rebuild_missing_data", {
                "methods_applied": methods,
                "missing_values_remaining": df.isna().sum().to_dict()
            })
            
            return df
            
        except Exception as e:
            logger.error(f"Error rebuilding missing data: {str(e)}")
            raise
    
    def standardize(self, columns: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Standardize numerical columns (zero mean, unit variance)
        
        Args:
            columns: List of columns to standardize. If None, standardizes all numeric columns.
        """
        try:
            if self.processed_data is None:
                raise ValueError("No data loaded. Import data first.")
                
            df = self.processed_data.copy()
            
            if columns is None:
                columns = df.select_dtypes(include=['int64', 'float64']).columns
            
            self._scaler = StandardScaler()
            df[columns] = self._scaler.fit_transform(df[columns])
            
            self.processed_data = df
            
            self.log_operation("standardize", {
                "columns_standardized": columns.tolist()
            })
            
            return df
            
        except Exception as e:
            logger.error(f"Error standardizing data: {str(e)}")
            raise
    
    def normalize(self, columns: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Normalize numerical columns to [0, 1] range
        
        Args:
            columns: List of columns to normalize. If None, normalizes all numeric columns.
        """
        try:
            if self.processed_data is None:
                raise ValueError("No data loaded. Import data first.")
                
            df = self.processed_data.copy()
            
            if columns is None:
                columns = df.select_dtypes(include=['int64', 'float64']).columns
            
            self._scaler = MinMaxScaler()
            df[columns] = self._scaler.fit_transform(df[columns])
            
            self.processed_data = df
            
            self.log_operation("normalize", {
                "columns_normalized": columns.tolist()
            })
            
            return df
            
        except Exception as e:
            logger.error(f"Error normalizing data: {str(e)}")
            raise
    
    def deduplicate(self, subset: Optional[List[str]] = None, 
                   keep: str = "first") -> pd.DataFrame:
        """
        Remove duplicate rows from the dataset
        
        Args:
            subset: Columns to consider for identifying duplicates
            keep: Which duplicate to keep ('first', 'last', False)
        """
        try:
            if self.processed_data is None:
                raise ValueError("No data loaded. Import data first.")
                
            df = self.processed_data.copy()
            original_shape = df.shape
            
            df = df.drop_duplicates(subset=subset, keep=keep)
            
            self.processed_data = df
            
            self.log_operation("deduplicate", {
                "columns_considered": subset,
                "keep_strategy": keep,
                "rows_removed": original_shape[0] - df.shape[0]
            })
            
            return df
            
        except Exception as e:
            logger.error(f"Error deduplicating data: {str(e)}")
            raise
    
    def verify_and_enrich(self, rules: Dict[str, Dict]) -> pd.DataFrame:
        """
        Verify data quality and enrich dataset based on rules
        
        Args:
            rules: Dictionary of rules for verification and enrichment
                  Example: {
                      "column_name": {
                          "type": "numeric",
                          "range": [0, 100],
                          "derived_column": "column_name_squared",
                          "derivation": "lambda x: x**2"
                      }
                  }
        """
        try:
            if self.processed_data is None:
                raise ValueError("No data loaded. Import data first.")
                
            df = self.processed_data.copy()
            verification_results = {}
            
            for column, rule in rules.items():
                if column not in df.columns:
                    logger.warning(f"Column {column} not found in dataset")
                    continue
                
                # Verify data type
                if "type" in rule:
                    if rule["type"] == "numeric":
                        df[column] = pd.to_numeric(df[column], errors='coerce')
                    elif rule["type"] == "datetime":
                        df[column] = pd.to_datetime(df[column], errors='coerce')
                
                # Verify range
                if "range" in rule and len(rule["range"]) == 2:
                    min_val, max_val = rule["range"]
                    mask = (df[column] >= min_val) & (df[column] <= max_val)
                    verification_results[f"{column}_in_range"] = mask.mean()
                
                # Create derived columns
                if "derived_column" in rule and "derivation" in rule:
                    try:
                        derivation_func = eval(rule["derivation"])
                        df[rule["derived_column"]] = df[column].apply(derivation_func)
                    except Exception as e:
                        logger.warning(f"Error creating derived column: {str(e)}")
            
            self.processed_data = df
            
            self.log_operation("verify_and_enrich", {
                "rules_applied": rules,
                "verification_results": verification_results
            })
            
            return df
            
        except Exception as e:
            logger.error(f"Error verifying and enriching data: {str(e)}")
            raise
    
    def export_data(self, format_type: str = "dataframe") -> Union[pd.DataFrame, str, Dict]:
        """
        Export processed data in various formats
        
        Args:
            format_type: Type of output ('dataframe', 'csv', 'json', 'dict')
        """
        try:
            if self.processed_data is None:
                raise ValueError("No data loaded. Import data first.")
                
            if format_type == "dataframe":
                return self.processed_data
            elif format_type == "csv":
                return self.processed_data.to_csv(index=False)
            elif format_type == "json":
                return self.processed_data.to_json(orient="records")
            elif format_type == "dict":
                return self.processed_data.to_dict(orient="records")
            else:
                raise ValueError(f"Unsupported format type: {format_type}")
            
        except Exception as e:
            logger.error(f"Error exporting data: {str(e)}")
            raise
    
    def get_cleaning_log(self) -> List[Dict]:
        """Get the complete cleaning operation log"""
        return self.cleaning_log 