import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Optional
import pandas as pd
import numpy as np

class FeeVisualization:
    """
    Management Fee visualization component that integrates with existing dashboard
    """
    
    def __init__(self):
        self.color_scheme = {
            'fee': '#3498db',      # Blue for fees
            'base': '#2ecc71',     # Green for base fees
            'incentive': '#e74c3c', # Red for incentive fees
            'threshold': '#f1c40f'  # Yellow for thresholds
        }
        
    def create_fee_structure_chart(self,
                                 data: pd.DataFrame,
                                 revenue_column: str,
                                 fee_column: str,
                                 title: str = "Management Fee Structure") -> go.Figure:
        """Create a scatter plot showing fee structure with trend line"""
        
        fig = go.Figure()
        
        # Add scatter plot of actual fees
        fig.add_trace(go.Scatter(
            x=data[revenue_column],
            y=data[fee_column],
            mode='markers',
            name='Actual Fees',
            marker=dict(
                color=self.color_scheme['fee'],
                size=8
            ),
            hovertemplate="Revenue: %{x:$,.2f}<br>Fee: %{y:$,.2f}<extra></extra>"
        ))
        
        # Add trend line
        z = np.polyfit(data[revenue_column], data[fee_column], 1)
        p = np.poly1d(z)
        
        fig.add_trace(go.Scatter(
            x=data[revenue_column],
            y=p(data[revenue_column]),
            mode='lines',
            name='Trend',
            line=dict(
                color=self.color_scheme['base'],
                dash='dash'
            )
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title="Revenue",
            yaxis_title="Management Fee",
            height=400,
            hovermode="closest"
        )
        
        return fig
        
    def create_sliding_scale_chart(self,
                                 breakpoints: pd.DataFrame,
                                 revenue_column: str,
                                 rate_column: str,
                                 title: str = "Fee Sliding Scale") -> go.Figure:
        """Create a step chart showing fee rate breakpoints"""
        
        fig = go.Figure()
        
        # Add step plot for fee rates
        fig.add_trace(go.Scatter(
            x=breakpoints[revenue_column],
            y=breakpoints[rate_column],
            mode='lines+markers',
            name='Fee Rate',
            line=dict(
                shape='hv',
                color=self.color_scheme['fee']
            ),
            marker=dict(
                symbol='circle',
                size=10,
                color=self.color_scheme['threshold']
            ),
            hovertemplate="Breakpoint: %{x:$,.2f}<br>Rate: %{y:.2f}%<extra></extra>"
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title="Revenue Breakpoint",
            yaxis_title="Fee Rate (%)",
            height=400,
            showlegend=False
        )
        
        return fig
        
    def create_fee_trend_chart(self,
                             data: pd.DataFrame,
                             date_column: str,
                             base_fee_column: str,
                             incentive_fee_column: str,
                             title: str = "Fee Composition Trend") -> go.Figure:
        """Create a stacked area chart showing fee composition over time"""
        
        fig = go.Figure()
        
        # Add base fee area
        fig.add_trace(go.Scatter(
            x=data[date_column],
            y=data[base_fee_column],
            name='Base Fee',
            fill='tonexty',
            mode='none',
            fillcolor=self.color_scheme['base'],
            hovertemplate="Base Fee: %{y:$,.2f}<extra></extra>"
        ))
        
        # Add incentive fee area
        fig.add_trace(go.Scatter(
            x=data[date_column],
            y=data[incentive_fee_column],
            name='Incentive Fee',
            fill='tonexty',
            mode='none',
            fillcolor=self.color_scheme['incentive'],
            hovertemplate="Incentive Fee: %{y:$,.2f}<extra></extra>"
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title="Date",
            yaxis_title="Fee Amount",
            height=400,
            hovermode="x unified"
        )
        
        return fig
        
    def create_fee_impact_chart(self,
                              data: pd.DataFrame,
                              date_column: str,
                              revenue_column: str,
                              total_fee_column: str,
                              title: str = "Fee Impact Analysis") -> go.Figure:
        """Create a dual-axis chart showing fee impact on revenue"""
        
        # Calculate fee percentage
        data['Fee_Percentage'] = (data[total_fee_column] / data[revenue_column] * 100).round(2)
        
        fig = go.Figure()
        
        # Add revenue bars
        fig.add_trace(go.Bar(
            x=data[date_column],
            y=data[revenue_column],
            name='Revenue',
            marker_color=self.color_scheme['base'],
            opacity=0.7,
            hovertemplate="Revenue: %{y:$,.2f}<extra></extra>"
        ))
        
        # Add fee percentage line
        fig.add_trace(go.Scatter(
            x=data[date_column],
            y=data['Fee_Percentage'],
            name='Fee %',
            yaxis="y2",
            line=dict(
                color=self.color_scheme['fee'],
                width=2
            ),
            hovertemplate="Fee %: %{y:.2f}%<extra></extra>"
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title="Date",
            yaxis_title="Revenue",
            yaxis2=dict(
                title="Fee % of Revenue",
                overlaying="y",
                side="right",
                tickformat=".1f"
            ),
            height=400,
            hovermode="x unified"
        )
        
        return fig
        
    def render_fee_summary(self,
                         data: pd.DataFrame,
                         revenue_column: str,
                         base_fee_column: str,
                         incentive_fee_column: str):
        """Render a summary of fee metrics"""
        
        st.subheader("Fee Analysis Summary")
        
        # Calculate metrics
        total_revenue = data[revenue_column].sum()
        total_base_fee = data[base_fee_column].sum()
        total_incentive_fee = data[incentive_fee_column].sum()
        total_fee = total_base_fee + total_incentive_fee
        avg_fee_pct = (total_fee / total_revenue * 100).round(2)
        
        # Display metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Total Fees",
                f"${total_fee:,.2f}",
                delta=f"{avg_fee_pct}% of Revenue"
            )
            
        with col2:
            st.metric(
                "Base Fees",
                f"${total_base_fee:,.2f}",
                delta=f"{(total_base_fee/total_fee*100):.1f}% of Total"
            )
            
        with col3:
            st.metric(
                "Incentive Fees",
                f"${total_incentive_fee:,.2f}",
                delta=f"{(total_incentive_fee/total_fee*100):.1f}% of Total"
            ) 