import streamlit as st
import pandas as pd
from datetime import datetime
from components.visualization.budget_charts import BudgetVisualization

def process_excel_file(file, file_type: str = "budget"):
    """Process Excel file with multiple sheets"""
    # Read all sheets
    xl = pd.ExcelFile(file)
    
    # Initialize empty list to store processed data
    processed_data = []
    
    # Process each sheet
    for sheet_name in xl.sheet_names:
        try:
            # Skip sheets that don't look like monthly data
            if sheet_name.lower() in ['instructions', 'reference', 'template']:
                continue
                
            # Read the sheet
            df = pd.read_excel(file, sheet_name=sheet_name)
            
            # Try to extract date from sheet name or look for date column
            try:
                # First try to parse sheet name as date
                sheet_date = pd.to_datetime(sheet_name)
            except:
                # If sheet name isn't a date, look for a date column
                date_cols = df.columns[df.columns.str.contains('date|month|period', case=False)]
                if len(date_cols) > 0:
                    sheet_date = pd.to_datetime(df[date_cols[0]].iloc[0])
                else:
                    st.warning(f"Could not determine date for sheet: {sheet_name}. Skipping.")
                    continue
            
            # Add period column if it doesn't exist
            if 'period' not in df.columns:
                df['period'] = sheet_date
            
            # Add sheet name for reference
            df['sheet_name'] = sheet_name
            df['data_type'] = file_type
            
            processed_data.append(df)
            
        except Exception as e:
            st.warning(f"Error processing sheet {sheet_name}: {str(e)}")
            continue
    
    if not processed_data:
        st.error("No valid data sheets found in the file.")
        return None
    
    # Combine all sheets
    combined_data = pd.concat(processed_data, ignore_index=True)
    return combined_data

def render_budget_dashboard():
    st.title("Budget Analysis Dashboard")
    
    # Initialize visualization component
    viz = BudgetVisualization()
    
    # File upload section
    st.header("Data Import")
    
    st.info("""
    Upload your budget and actual data files. Each file should be an Excel workbook (.xlsx) containing multiple monthly sheets.
    
    **File Format Requirements:**
    - Each workbook should contain monthly data in separate sheets
    - Sheet names can be dates (e.g., '2024-01') or standard names (e.g., 'January 2024')
    - Each sheet should have consistent column names across all months
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        budget_file = st.file_uploader(
            "Upload Budget Data (Excel workbook)",
            type=["xlsx"],
            key="budget_upload",
            help="Select an Excel file containing monthly budget data in separate sheets"
        )
        if budget_file:
            st.success(f"✓ Budget file '{budget_file.name}' uploaded successfully")
        
    with col2:
        actual_file = st.file_uploader(
            "Upload Actual Data (Excel workbook)",
            type=["xlsx"],
            key="actual_upload",
            help="Select an Excel file containing monthly actual data in separate sheets"
        )
        if actual_file:
            st.success(f"✓ Actual file '{actual_file.name}' uploaded successfully")
    
    if budget_file is not None or actual_file is not None:
        if budget_file is None:
            st.warning("⚠️ Please upload the budget data file")
        if actual_file is None:
            st.warning("⚠️ Please upload the actual data file")
            
    if budget_file is not None and actual_file is not None:
        try:
            # Process both files
            with st.spinner("Processing budget data..."):
                budget_data = process_excel_file(budget_file, "budget")
            with st.spinner("Processing actual data..."):
                actual_data = process_excel_file(actual_file, "actual")
            
            if budget_data is None or actual_data is None:
                st.error("Please ensure both files contain valid monthly data sheets.")
                return
                
            # Show data preview
            st.subheader("Data Preview")
            col1, col2 = st.columns(2)
            with col1:
                budget_sheets = budget_data['sheet_name'].unique()
                st.write("Budget Data Sheets:", len(budget_sheets), "sheets found")
                st.write(sorted(budget_sheets))
            with col2:
                actual_sheets = actual_data['sheet_name'].unique()
                st.write("Actual Data Sheets:", len(actual_sheets), "sheets found")
                st.write(sorted(actual_sheets))
                
            # Check for sheet count mismatch
            if len(budget_sheets) != len(actual_sheets):
                st.warning(f"⚠️ Number of sheets differs between budget ({len(budget_sheets)}) and actual ({len(actual_sheets)}) data")
            
            # Configuration section
            st.header("Analysis Configuration")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                # Always use 'period' as date column
                date_col = 'period'
                st.info(f"Using '{date_col}' as date column")
                
            with col2:
                category_col = st.selectbox(
                    "Select Category Column",
                    [col for col in budget_data.columns if col not in ['period', 'sheet_name', 'data_type']],
                    key="category_column"
                )
                
            with col3:
                amount_cols = st.multiselect(
                    "Select Amount Columns",
                    [col for col in budget_data.columns if col not in ['period', 'sheet_name', 'data_type', category_col]],
                    key="amount_columns"
                )
                
            if st.button("Generate Analysis"):
                # Ensure date format consistency
                budget_data[date_col] = pd.to_datetime(budget_data[date_col])
                actual_data[date_col] = pd.to_datetime(actual_data[date_col])
                
                # Calculate variances
                merged_data = pd.merge(
                    budget_data,
                    actual_data,
                    on=[date_col, category_col],
                    suffixes=('_budget', '_actual')
                )
                
                # Create tabs for different views
                tab1, tab2, tab3, tab4 = st.tabs([
                    "Overview",
                    "Variance Analysis",
                    "Trend Analysis",
                    "YTD Performance"
                ])
                
                with tab1:
                    st.subheader("Budget vs. Actual Overview")
                    
                    # Summary metrics
                    for col in amount_cols:
                        budget_col = f"{col}_budget"
                        actual_col = f"{col}_actual"
                        variance_col = f"{col}_variance"
                        
                        merged_data[variance_col] = (
                            merged_data[actual_col] - merged_data[budget_col]
                        )
                        
                        # Render YTD summary
                        viz.render_ytd_summary(
                            merged_data,
                            budget_col,
                            actual_col,
                            variance_col
                        )
                        
                        # Render trend chart
                        st.plotly_chart(
                            viz.create_budget_vs_actual_chart(
                                merged_data,
                                date_col,
                                budget_col,
                                actual_col,
                                title=f"{col} - Budget vs. Actual Trend"
                            ),
                            use_container_width=True
                        )
                        
                with tab2:
                    st.subheader("Variance Analysis")
                    
                    # Variance threshold control
                    threshold = st.slider(
                        "Variance Threshold (%)",
                        min_value=1.0,
                        max_value=20.0,
                        value=5.0,
                        step=0.5
                    )
                    
                    for col in amount_cols:
                        variance_col = f"{col}_variance"
                        
                        # Render variance summary
                        viz.render_variance_summary(
                            merged_data,
                            variance_col,
                            threshold
                        )
                        
                        # Render waterfall chart
                        st.plotly_chart(
                            viz.create_variance_waterfall(
                                merged_data,
                                category_col,
                                f"{col}_budget",
                                f"{col}_actual",
                                title=f"{col} - Variance Breakdown"
                            ),
                            use_container_width=True
                        )
                        
                with tab3:
                    st.subheader("Trend Analysis")
                    
                    for col in amount_cols:
                        variance_col = f"{col}_variance"
                        
                        # Render heatmap
                        st.plotly_chart(
                            viz.create_variance_heatmap(
                                merged_data,
                                category_col,
                                date_col,
                                variance_col,
                                title=f"{col} - Variance Heatmap"
                            ),
                            use_container_width=True
                        )
                        
                with tab4:
                    st.subheader("YTD Performance")
                    
                    # Group by category
                    ytd_data = merged_data.groupby(category_col).agg({
                        col: 'sum' for col in merged_data.columns
                        if col.endswith(('_budget', '_actual', '_variance'))
                    }).reset_index()
                    
                    # Format YTD data with custom styling
                    def style_negative_values(val):
                        """Style negative values in red, positive in green"""
                        if isinstance(val, (int, float)):
                            color = 'red' if val < 0 else 'green' if val > 0 else 'white'
                            return f'color: {color}'
                        return ''

                    # Apply styling to variance columns
                    variance_cols = [col for col in ytd_data.columns if col.endswith('_variance')]
                    styled_ytd = ytd_data.style.applymap(
                        style_negative_values,
                        subset=variance_cols
                    ).format({
                        col: "{:,.2f}" for col in ytd_data.select_dtypes(include=['float64']).columns
                    })
                    
                    # Display YTD data
                    st.dataframe(styled_ytd, height=400)
                    
        except Exception as e:
            st.error(f"Error processing data: {str(e)}")
            
    else:
        st.info("Please upload both budget and actual data files to begin analysis. Each file should contain monthly sheets.")

# Call the dashboard render function
if __name__ == "__main__":
    render_budget_dashboard() 