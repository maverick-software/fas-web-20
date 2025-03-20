# Frontend Component Documentation

## Directory Purpose
Contains the Streamlit-based user interface for the Financial Analysis System, providing data upload, visualization, and command input capabilities.

## Structure
- `app.py` - Main Streamlit application entry point
- `requirements.txt` - Frontend dependencies
- `/venv/` - Python virtual environment (created by setup.bat)

## Key Files
- `app.py`: Main application file containing:
  - File upload interface
  - Data table display
  - Visualization components
  - Natural language command input
  - Dark mode styling

## Dependencies
Specific versions used:
- streamlit==1.22.0
- plotly==5.13.0
- pandas==1.3.0
- numpy==1.21.0
- openpyxl==3.0.9

## Features
- Dark mode interface
- Drag-and-drop file upload (CSV/XLSX)
- Real-time data visualization
- Natural language command processing
- Interactive data table view

## Server Configuration
- Port: 8501
- Host: localhost
- URL: http://localhost:8501 