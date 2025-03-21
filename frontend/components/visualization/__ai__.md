# Visualization Components

## Purpose
This folder contains visualization components that create interactive charts and dashboards for financial analysis.

## Structure
- `fee_charts.py`: Management fee visualization component
- `noi_charts.py`: NOI (Net Operating Income) visualization component

## Key Classes

### FeeVisualization
Located in `fee_charts.py`
- Creates interactive charts for management fee analysis
- Includes fee structure, trends, and impact visualizations
- Uses consistent color scheme for visual clarity

Methods:
- `create_fee_structure_chart`: Scatter plot of fees vs revenue
- `create_sliding_scale_chart`: Step chart of fee rate breakpoints
- `create_fee_trend_chart`: Stacked area chart of fee composition
- `create_fee_impact_chart`: Dual-axis chart of fee impact
- `render_fee_summary`: Displays key fee metrics

### NOIVisualization
Located in `noi_charts.py`
- Creates interactive charts for NOI analysis
- Includes property comparison and trend analysis
- Uses property-specific color scheme

Methods:
- `create_monthly_trend`: Line chart of NOI trends
- `create_operating_margin_chart`: Stacked bar chart with margin
- `create_yoy_comparison`: Bar chart of year-over-year growth
- `render_property_comparison`: Comprehensive property dashboard

## Dependencies
- Streamlit: UI framework
- Plotly: Interactive charts
- Pandas: Data manipulation
- NumPy: Numerical operations

## Best Practices
1. Maintain consistent color schemes across visualizations
2. Use type hints for better code maintainability
3. Include hover information for all charts
4. Ensure responsive design for all components
5. Follow modular design principles

## Related Documentation
- [Management Fee Analysis Feature](../../docs/features/management_fee_analysis.md)
- [Project Documentation](../../docs/README.md) 