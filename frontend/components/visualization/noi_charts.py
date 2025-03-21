import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Optional
import pandas as pd
import numpy as np

class NOIVisualization:
    """
    NOI Analysis visualization component that integrates with existing dashboard
    """
    
    def __init__(self):
        self.color_scheme = {
            'blanco': '#2ecc71',    # Green for Blanco
            'rio': '#3498db',       # Blue for Rio
            'revenue': '#f1c40f',   # Yellow for Revenue
            'expenses': '#e74c3c',  # Red for Expenses
            'noi': '#9b59b6'        # Purple for NOI
        }
        
    def create_monthly_trend(self,
                           data: pd.DataFrame,
                           date_column: str,
                           noi_column: str,
                           property_column: str,
                           title: str = "Monthly NOI Trends") -> go.Figure:
        """Create a line chart showing monthly NOI trends by property"""
        
        fig = go.Figure()
        
        for property_name in data[property_column].unique():
            property_data = data[data[property_column] == property_name]
            
            fig.add_trace(go.Scatter(
                x=property_data[date_column],
                y=property_data[noi_column],
                name=property_name,
                line=dict(
                    color=self.color_scheme['blanco'] if property_name == 'Blanco' 
                    else self.color_scheme['rio'],
                    width=2
                ),
                hovertemplate=f"{property_name}<br>NOI: %{{y:$,.2f}}<br>Date: %{{x}}<extra></extra>"
            ))
            
        fig.update_layout(
            title=title,
            xaxis_title="Date",
            yaxis_title="NOI",
            hovermode="x unified",
            height=400
        )
        
        return fig
        
    def create_operating_margin_chart(self,
                                    data: pd.DataFrame,
                                    date_column: str,
                                    revenue_column: str,
                                    expense_column: str,
                                    property_column: str,
                                    title: str = "Operating Margin Analysis") -> go.Figure:
        """Create a stacked bar chart showing revenue, expenses, and margin"""
        
        # Calculate operating margin
        data['Operating_Margin'] = (
            (data[revenue_column] - data[expense_column]) / data[revenue_column] * 100
        ).round(2)
        
        fig = go.Figure()
        
        for property_name in data[property_column].unique():
            property_data = data[data[property_column] == property_name]
            
            # Add revenue bars
            fig.add_trace(go.Bar(
                x=property_data[date_column],
                y=property_data[revenue_column],
                name=f"{property_name} Revenue",
                marker_color=self.color_scheme['revenue'],
                hovertemplate="Revenue: %{y:$,.2f}<extra></extra>"
            ))
            
            # Add expense bars
            fig.add_trace(go.Bar(
                x=property_data[date_column],
                y=property_data[expense_column],
                name=f"{property_name} Expenses",
                marker_color=self.color_scheme['expenses'],
                hovertemplate="Expenses: %{y:$,.2f}<extra></extra>"
            ))
            
            # Add margin line
            fig.add_trace(go.Scatter(
                x=property_data[date_column],
                y=property_data['Operating_Margin'],
                name=f"{property_name} Margin",
                yaxis="y2",
                line=dict(color=self.color_scheme['noi'], width=2),
                hovertemplate="Margin: %{y:.1f}%<extra></extra>"
            ))
            
        fig.update_layout(
            title=title,
            xaxis_title="Date",
            yaxis_title="Amount ($)",
            yaxis2=dict(
                title="Operating Margin (%)",
                overlaying="y",
                side="right",
                range=[0, 100]
            ),
            barmode='group',
            height=500,
            hovermode="x unified"
        )
        
        return fig
        
    def create_yoy_comparison(self,
                            data: pd.DataFrame,
                            date_column: str,
                            noi_column: str,
                            property_column: str,
                            title: str = "Year-over-Year Growth") -> go.Figure:
        """Create a bar chart showing year-over-year NOI growth"""
        
        # Calculate YoY growth
        data['Year'] = pd.to_datetime(data[date_column]).dt.year
        data['Month'] = pd.to_datetime(data[date_column]).dt.month
        
        yoy_data = []
        for property_name in data[property_column].unique():
            property_data = data[data[property_column] == property_name].copy()
            property_data['YoY_Growth'] = property_data.groupby('Month')[noi_column].pct_change(12) * 100
            yoy_data.append(property_data)
            
        yoy_data = pd.concat(yoy_data)
        
        fig = go.Figure()
        
        for property_name in yoy_data[property_column].unique():
            property_data = yoy_data[yoy_data[property_column] == property_name]
            
            fig.add_trace(go.Bar(
                x=property_data[date_column],
                y=property_data['YoY_Growth'],
                name=property_name,
                marker_color=self.color_scheme['blanco'] if property_name == 'Blanco'
                else self.color_scheme['rio'],
                hovertemplate=f"{property_name}<br>Growth: %{{y:.1f}}%<br>Date: %{{x}}<extra></extra>"
            ))
            
        fig.update_layout(
            title=title,
            xaxis_title="Date",
            yaxis_title="YoY Growth (%)",
            barmode='group',
            height=400,
            hovermode="x unified"
        )
        
        return fig
        
    def render_property_comparison(self,
                                 data: pd.DataFrame,
                                 date_column: str,
                                 noi_column: str,
                                 revenue_column: str,
                                 expense_column: str,
                                 property_column: str):
        """Render a comprehensive property comparison dashboard"""
        
        st.subheader("Property Performance Comparison")
        
        # Calculate key metrics
        metrics = {}
        for property_name in data[property_column].unique():
            property_data = data[data[property_column] == property_name]
            metrics[property_name] = {
                'Current_NOI': property_data[noi_column].iloc[-1],
                'Avg_NOI': property_data[noi_column].mean(),
                'Operating_Margin': (
                    (property_data[revenue_column].sum() - property_data[expense_column].sum()) /
                    property_data[revenue_column].sum() * 100
                ).round(2)
            }
            
        # Display metrics
        col1, col2 = st.columns(2)
        
        for idx, (property_name, metric) in enumerate(metrics.items()):
            with col1 if idx == 0 else col2:
                st.markdown(f"### {property_name}")
                st.metric(
                    "Current NOI",
                    f"${metric['Current_NOI']:,.2f}",
                    delta=f"${metric['Current_NOI'] - metric['Avg_NOI']:,.2f} vs Avg"
                )
                st.metric(
                    "Operating Margin",
                    f"{metric['Operating_Margin']}%"
                )
                
        # Add comparison charts
        st.plotly_chart(
            self.create_monthly_trend(
                data,
                date_column,
                noi_column,
                property_column
            ),
            use_container_width=True
        )
        
        st.plotly_chart(
            self.create_yoy_comparison(
                data,
                date_column,
                noi_column,
                property_column
            ),
            use_container_width=True
        ) 