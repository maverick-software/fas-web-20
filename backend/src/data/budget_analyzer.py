import pandas as pd
import numpy as np
from typing import Dict, List, Union, Optional
from datetime import datetime
import logging
from .data_processor import DataProcessor

logger = logging.getLogger(__name__)

class BudgetAnalyzer:
    """
    Budget vs. Actual analysis module that works alongside existing DataProcessor
    """
    
    def __init__(self, data_processor: Optional[DataProcessor] = None):
        self.data_processor = data_processor or DataProcessor()
        self.budget_data = None
        self.actual_data = None
        self.variance_data = None
        self.analysis_log = []
        
    def log_analysis(self, operation: str, details: Dict):
        """Log a budget analysis operation"""
        self.analysis_log.append({
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "details": details
        })
        
    def import_budget_data(self, budget_data: Union[pd.DataFrame, str, Dict],
                          format_type: str = "dataframe") -> pd.DataFrame:
        """Import and validate budget data"""
        try:
            self.budget_data = self.data_processor.import_data(budget_data, format_type)
            self.log_analysis("import_budget", {"status": "success"})
            return self.budget_data
        except Exception as e:
            self.log_analysis("import_budget", {"status": "error", "message": str(e)})
            raise
            
    def import_actual_data(self, actual_data: Union[pd.DataFrame, str, Dict],
                          format_type: str = "dataframe") -> pd.DataFrame:
        """Import and validate actual data"""
        try:
            self.actual_data = self.data_processor.import_data(actual_data, format_type)
            self.log_analysis("import_actual", {"status": "success"})
            return self.actual_data
        except Exception as e:
            self.log_analysis("import_actual", {"status": "error", "message": str(e)})
            raise
            
    def calculate_variances(self, 
                          date_column: str,
                          amount_columns: List[str],
                          category_columns: Optional[List[str]] = None) -> pd.DataFrame:
        """Calculate variances between budget and actual data"""
        if self.budget_data is None or self.actual_data is None:
            raise ValueError("Both budget and actual data must be imported first")
            
        try:
            # Ensure consistent date format
            for df in [self.budget_data, self.actual_data]:
                df[date_column] = pd.to_datetime(df[date_column])
            
            # Merge budget and actual data
            merge_columns = [date_column] + (category_columns or [])
            merged_data = pd.merge(
                self.budget_data,
                self.actual_data,
                on=merge_columns,
                suffixes=('_budget', '_actual')
            )
            
            # Calculate variances
            for col in amount_columns:
                budget_col = f"{col}_budget"
                actual_col = f"{col}_actual"
                variance_col = f"{col}_variance"
                variance_pct_col = f"{col}_variance_pct"
                
                merged_data[variance_col] = merged_data[actual_col] - merged_data[budget_col]
                merged_data[variance_pct_col] = (
                    (merged_data[variance_col] / merged_data[budget_col].abs()) * 100
                ).round(2)
                
            self.variance_data = merged_data
            self.log_analysis("calculate_variances", {"status": "success"})
            return self.variance_data
            
        except Exception as e:
            self.log_analysis("calculate_variances", {
                "status": "error",
                "message": str(e)
            })
            raise
            
    def get_significant_variances(self,
                                threshold_pct: float = 5.0,
                                variance_columns: Optional[List[str]] = None) -> pd.DataFrame:
        """Identify significant variances based on threshold"""
        if self.variance_data is None:
            raise ValueError("Variance data not calculated yet")
            
        try:
            # Get variance percentage columns
            if variance_columns is None:
                variance_columns = [col for col in self.variance_data.columns 
                                  if col.endswith('_variance_pct')]
            
            # Create mask for significant variances
            mask = pd.DataFrame(False, index=self.variance_data.index,
                              columns=variance_columns)
            
            for col in variance_columns:
                mask[col] = self.variance_data[col].abs() >= threshold_pct
                
            # Filter data
            significant_variances = self.variance_data[mask.any(axis=1)]
            
            self.log_analysis("get_significant_variances", {
                "status": "success",
                "threshold": threshold_pct,
                "count": len(significant_variances)
            })
            
            return significant_variances
            
        except Exception as e:
            self.log_analysis("get_significant_variances", {
                "status": "error",
                "message": str(e)
            })
            raise
            
    def calculate_ytd_performance(self,
                                date_column: str,
                                amount_columns: List[str],
                                category_columns: Optional[List[str]] = None) -> pd.DataFrame:
        """Calculate year-to-date performance metrics"""
        if self.variance_data is None:
            raise ValueError("Variance data not calculated yet")
            
        try:
            # Group by category columns if provided
            group_cols = category_columns or []
            
            # Calculate YTD sums
            ytd_data = self.variance_data.groupby(
                group_cols + [pd.Grouper(key=date_column, freq='YTD')]
            ).agg({
                col: 'sum' for col in self.variance_data.columns
                if any(col.endswith(suffix) 
                      for suffix in ['_budget', '_actual', '_variance'])
            }).reset_index()
            
            # Calculate YTD percentages
            for col in amount_columns:
                budget_col = f"{col}_budget"
                variance_col = f"{col}_variance"
                ytd_data[f"{col}_ytd_pct"] = (
                    (ytd_data[variance_col] / ytd_data[budget_col].abs()) * 100
                ).round(2)
                
            self.log_analysis("calculate_ytd_performance", {"status": "success"})
            return ytd_data
            
        except Exception as e:
            self.log_analysis("calculate_ytd_performance", {
                "status": "error",
                "message": str(e)
            })
            raise
            
    def get_analysis_log(self) -> List[Dict]:
        """Return the analysis operation log"""
        return self.analysis_log 