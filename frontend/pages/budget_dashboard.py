import streamlit as st
import pandas as pd
from datetime import datetime
from components.visualization.budget_charts import BudgetVisualization

def render_budget_dashboard():
    st.title("Budget Analysis Dashboard")
    
    # Initialize visualization component
    viz = BudgetVisualization()
    
    # File upload section
    st.header("Data Import")
    
    col1, col2 = st.columns(2)
    
    with col1:
        budget_file = st.file_uploader(
            "Upload Budget Data (Excel/CSV)",
            type=["xlsx", "csv"],
            key="budget_upload"
        )
        
    with col2:
        actual_file = st.file_uploader(
            "Upload Actual Data (Excel/CSV)",
            type=["xlsx", "csv"],
            key="actual_upload"
        )
        
    if budget_file is not None and actual_file is not None:
        try:
            # Load data
            if budget_file.name.endswith('.csv'):
                budget_data = pd.read_csv(budget_file)
            else:
                budget_data = pd.read_excel(budget_file)
                
            if actual_file.name.endswith('.csv'):
                actual_data = pd.read_csv(actual_file)
            else:
                actual_data = pd.read_excel(actual_file)
                
            # Configuration section
            st.header("Analysis Configuration")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                date_col = st.selectbox(
                    "Select Date Column",
                    budget_data.columns,
                    key="date_column"
                )
                
            with col2:
                category_col = st.selectbox(
                    "Select Category Column",
                    budget_data.columns,
                    key="category_column"
                )
                
            with col3:
                amount_cols = st.multiselect(
                    "Select Amount Columns",
                    budget_data.columns,
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
                    
                    # Display YTD data
                    st.dataframe(
                        ytd_data.style.background_gradient(
                            cmap='RdYlGn',
                            subset=[col for col in ytd_data.columns
                                   if col.endswith('_variance')]
                        ),
                        height=400
                    )
                    
        except Exception as e:
            st.error(f"Error processing data: {str(e)}")
            
    else:
        st.info("Please upload both budget and actual data files to begin analysis.")

# Call the dashboard render function
if __name__ == "__main__":
    render_budget_dashboard() 