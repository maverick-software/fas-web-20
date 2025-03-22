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
        
        # Handle duplicate categories by taking the sum
        agg_data = data.groupby(category_column).agg({
            budget_column: 'sum',
            actual_column: 'sum'
        }).reset_index()
        
        # Calculate variances
        variances = agg_data[actual_column] - agg_data[budget_column]
        
        # Create waterfall chart
        fig = go.Figure(go.Waterfall(
            name="Variance",
            orientation="v",
            measure=["relative"] * len(agg_data),
            x=agg_data[category_column],
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
            height=350,  # Reduced height
            margin=dict(t=30, b=30)  # Reduced margins
        )
        
        return fig
        
    def create_budget_vs_actual_chart(self,
                                    data: pd.DataFrame,
                                    date_column: str,
                                    budget_column: str,
                                    actual_column: str,
                                    title: str = "Budget vs. Actual Trend") -> go.Figure:
        """Create a line chart comparing budget to actual over time"""
        
        # Sort data by date
        data = data.sort_values(date_column)
        
        # Group by date and category
        agg_data = data.groupby(date_column).agg({
            budget_column: 'sum',
            actual_column: 'sum'
        }).reset_index()
        
        # Calculate cumulative values and variances
        agg_data['cumulative_budget'] = agg_data[budget_column].cumsum()
        agg_data['cumulative_actual'] = agg_data[actual_column].cumsum()
        agg_data['variance'] = agg_data[actual_column] - agg_data[budget_column]
        agg_data['cumulative_variance'] = agg_data['cumulative_actual'] - agg_data['cumulative_budget']
        
        fig = go.Figure()
        
        # Add monthly bars for variance
        fig.add_trace(go.Bar(
            x=agg_data[date_column],
            y=agg_data['variance'],
            name="Monthly Variance",
            marker_color=[self.color_scheme['positive'] if x >= 0 else self.color_scheme['negative'] for x in agg_data['variance']],
            opacity=0.3,
            hovertemplate="Date: %{x}<br>Variance: $%{y:,.2f}<extra></extra>"
        ))
        
        # Add budget line
        fig.add_trace(go.Scatter(
            x=agg_data[date_column],
            y=agg_data[budget_column],
            name="Monthly Budget",
            line=dict(color=self.color_scheme['neutral'], width=2),
            hovertemplate="Budget: $%{y:,.2f}<br>Date: %{x}<extra></extra>"
        ))
        
        # Add actual line
        fig.add_trace(go.Scatter(
            x=agg_data[date_column],
            y=agg_data[actual_column],
            name="Monthly Actual",
            line=dict(color=self.color_scheme['actual'], width=2),
            hovertemplate="Actual: $%{y:,.2f}<br>Date: %{x}<extra></extra>"
        ))
        
        # Add cumulative lines
        fig.add_trace(go.Scatter(
            x=agg_data[date_column],
            y=agg_data['cumulative_budget'],
            name="Cumulative Budget",
            line=dict(color=self.color_scheme['neutral'], width=2, dash='dot'),
            hovertemplate="Cum. Budget: $%{y:,.2f}<br>Date: %{x}<extra></extra>"
        ))
        
        fig.add_trace(go.Scatter(
            x=agg_data[date_column],
            y=agg_data['cumulative_actual'],
            name="Cumulative Actual",
            line=dict(color=self.color_scheme['actual'], width=2, dash='dot'),
            hovertemplate="Cum. Actual: $%{y:,.2f}<br>Date: %{x}<extra></extra>"
        ))
        
        # Update layout
        fig.update_layout(
            title=title,
            xaxis_title="Date",
            yaxis_title="Amount ($)",
            hovermode="x unified",
            height=400,
            barmode='relative',
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            # Add range selector
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=3, label="3M", step="month", stepmode="backward"),
                        dict(count=6, label="6M", step="month", stepmode="backward"),
                        dict(count=1, label="YTD", step="year", stepmode="todate"),
                        dict(count=1, label="1Y", step="year", stepmode="backward"),
                        dict(step="all", label="All")
                    ])
                ),
                rangeslider=dict(visible=True),
                type="date"
            )
        )
        
        return fig
        
    def create_variance_heatmap(self,
                              data: pd.DataFrame,
                              category_column: str,
                              date_column: str,
                              variance_column: str,
                              title: str = "Variance Heatmap") -> go.Figure:
        """Create a heatmap showing variances across categories and time"""
        
        # Handle duplicate entries by taking the sum
        agg_data = data.groupby([category_column, date_column])[variance_column].sum().reset_index()
        
        # Pivot data for heatmap
        pivot_data = agg_data.pivot(
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
            height=350,  # Reduced height
            xaxis_title="Date",
            yaxis_title="Category",
            margin=dict(t=30, b=30)  # Reduced margins
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
            # Format variance data with custom styling
            def style_negative_values(val):
                """Style negative values in red, positive in green"""
                if isinstance(val, (int, float)):
                    color = 'red' if val < 0 else 'green' if val > 0 else 'white'
                    return f'color: {color}'
                return ''

            # Apply styling to variance column
            styled_variances = significant_variances.style.applymap(
                style_negative_values,
                subset=[variance_column]
            ).format({
                col: "{:,.2f}" for col in significant_variances.select_dtypes(include=['float64']).columns
            })
            
            st.dataframe(styled_variances, height=400)
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