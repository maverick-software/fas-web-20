import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Optional
import pandas as pd
import numpy as np

class BudgetVisualization:
    """
    Budget vs. Actual visualization component that integrates with existing dashboard
    """
    
    def __init__(self):
        self.color_scheme = {
            'positive': '#2ecc71',  # Green for favorable variances
            'negative': '#e74c3c',  # Red for unfavorable variances
            'neutral': '#3498db',   # Blue for budget/baseline
            'actual': '#f1c40f'     # Yellow for actual values
        }
        
    def create_variance_waterfall(self,
                                data: pd.DataFrame,
                                category_column: str,
                                budget_column: str,
                                actual_column: str,
                                title: str = "Budget vs. Actual Waterfall") -> go.Figure:
        """Create a waterfall chart showing budget to actual variance breakdown"""
        
        # Calculate variances
        variances = data[actual_column] - data[budget_column]
        
        # Create waterfall chart
        fig = go.Figure(go.Waterfall(
            name="Variance",
            orientation="v",
            measure=["relative"] * len(data),
            x=data[category_column],
            y=variances,
            connector={"line": {"color": "rgb(63, 63, 63)"}},
            decreasing={"marker": {"color": self.color_scheme['negative']}},
            increasing={"marker": {"color": self.color_scheme['positive']}},
            text=variances.round(2),
            textposition="outside"
        ))
        
        fig.update_layout(
            title=title,
            showlegend=True,
            height=500
        )
        
        return fig
        
    def create_budget_vs_actual_chart(self,
                                    data: pd.DataFrame,
                                    date_column: str,
                                    budget_column: str,
                                    actual_column: str,
                                    title: str = "Budget vs. Actual Trend") -> go.Figure:
        """Create a line chart comparing budget to actual over time"""
        
        fig = go.Figure()
        
        # Add budget line
        fig.add_trace(go.Scatter(
            x=data[date_column],
            y=data[budget_column],
            name="Budget",
            line=dict(color=self.color_scheme['neutral'], width=2),
            hovertemplate="Budget: %{y:,.2f}<br>Date: %{x}<extra></extra>"
        ))
        
        # Add actual line
        fig.add_trace(go.Scatter(
            x=data[date_column],
            y=data[actual_column],
            name="Actual",
            line=dict(color=self.color_scheme['actual'], width=2),
            hovertemplate="Actual: %{y:,.2f}<br>Date: %{x}<extra></extra>"
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title="Date",
            yaxis_title="Amount",
            hovermode="x unified",
            height=400
        )
        
        return fig
        
    def create_variance_heatmap(self,
                              data: pd.DataFrame,
                              category_column: str,
                              date_column: str,
                              variance_column: str,
                              title: str = "Variance Heatmap") -> go.Figure:
        """Create a heatmap showing variances across categories and time"""
        
        # Pivot data for heatmap
        pivot_data = data.pivot(
            index=category_column,
            columns=date_column,
            values=variance_column
        )
        
        # Create heatmap
        fig = go.Figure(data=go.Heatmap(
            z=pivot_data.values,
            x=pivot_data.columns,
            y=pivot_data.index,
            colorscale='RdYlGn',  # Red for negative, Yellow for neutral, Green for positive
            hoverongaps=False,
            hovertemplate="Category: %{y}<br>Date: %{x}<br>Variance: %{z:,.2f}<extra></extra>"
        ))
        
        fig.update_layout(
            title=title,
            height=400,
            xaxis_title="Date",
            yaxis_title="Category"
        )
        
        return fig
        
    def render_variance_summary(self,
                              data: pd.DataFrame,
                              variance_column: str,
                              threshold: float = 5.0):
        """Render a summary of significant variances"""
        
        significant_variances = data[abs(data[variance_column]) >= threshold]
        
        st.subheader("Significant Variances")
        
        # Summary metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Total Variances",
                f"{len(significant_variances):,}",
                delta=None
            )
            
        with col2:
            positive_vars = len(significant_variances[significant_variances[variance_column] > 0])
            st.metric(
                "Favorable",
                f"{positive_vars:,}",
                delta=f"{(positive_vars/len(significant_variances)*100):.1f}%"
            )
            
        with col3:
            negative_vars = len(significant_variances[significant_variances[variance_column] < 0])
            st.metric(
                "Unfavorable",
                f"{negative_vars:,}",
                delta=f"-{(negative_vars/len(significant_variances)*100):.1f}%",
                delta_color="inverse"
            )
            
        # Variance table
        if not significant_variances.empty:
            st.dataframe(
                significant_variances.style.background_gradient(
                    cmap='RdYlGn',
                    subset=[variance_column]
                ),
                height=400
            )
        else:
            st.info("No significant variances found.")
            
    def render_ytd_summary(self,
                          data: pd.DataFrame,
                          budget_column: str,
                          actual_column: str,
                          variance_column: str):
        """Render year-to-date performance summary"""
        
        st.subheader("Year-to-Date Performance")
        
        # Calculate YTD totals
        ytd_budget = data[budget_column].sum()
        ytd_actual = data[actual_column].sum()
        ytd_variance = data[variance_column].sum()
        ytd_variance_pct = (ytd_variance / abs(ytd_budget)) * 100
        
        # Display metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "YTD Budget",
                f"${ytd_budget:,.2f}"
            )
            
        with col2:
            st.metric(
                "YTD Actual",
                f"${ytd_actual:,.2f}",
                delta=f"${ytd_variance:,.2f}"
            )
            
        with col3:
            st.metric(
                "YTD Variance %",
                f"{ytd_variance_pct:.1f}%",
                delta=f"{ytd_variance_pct:.1f}%",
                delta_color="normal" if ytd_variance_pct >= 0 else "inverse"
            ) 