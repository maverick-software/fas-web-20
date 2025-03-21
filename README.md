# Financial Analysis System v2.0

An AI-powered real-time data visualization and manipulation tool designed for financial analysts and business professionals. This tool enables seamless dataset analysis through natural language commands and interactive visualizations.

## Features

### Data Management
- Upload and process CSV/XLSX files
- Natural language data manipulation
- Dark mode user interface
- RESTful API backend

### Financial Analysis
- **Management Fee Analysis**
  - Fee composition tracking
  - Revenue-based fee structure analysis
  - Sliding scale fee visualization
  - Fee impact assessment
  - Interactive fee metrics dashboard
- **NOI Analysis**
  - Monthly trend tracking
  - Operating margin analysis
  - Year-over-year comparisons
  - Property performance dashboard

### Visualization
- Real-time interactive charts
- Customizable date ranges
- Summary metrics displays
- Multi-tab analysis views
- Responsive design

## Prerequisites
- Python 3.11.4 or higher
- Windows 10 or higher

## Quick Start
1. Clone this repository
2. Run `setup.bat` to initialize the development environment
3. Run `start_backend.bat` to start the API server
4. Run `start_frontend.bat` to start the user interface
5. Access the application at http://localhost:8501

## Project Structure
```
ai-data-tool/
├── frontend/          # Streamlit user interface
│   ├── pages/        # Application pages
│   └── components/   # Reusable UI components
│       └── visualization/  # Chart components
├── backend/          # FastAPI server
├── docs/            # Documentation
│   └── features/    # Feature documentation
├── setup.bat        # Environment setup script
├── start_frontend.bat # Frontend server startup
└── start_backend.bat  # Backend server startup
```

## Documentation
- Frontend Documentation: [frontend/__ai__.md](frontend/__ai__.md)
- Backend Documentation: [backend/__ai__.md](backend/__ai__.md)
- Feature Documentation:
  - [Management Fee Analysis](docs/features/management_fee_analysis.md)
- Change Log: [_change.logs](_change.logs)

## API Documentation
Once the backend server is running, access:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Development
For detailed development guidelines and protocols, see:
- `.cursor/rules/protocols/documentation.mdc`
- `.cursor/rules/compliance.mdc`

## Dependencies
- Streamlit: UI framework
- FastAPI: Backend server
- Plotly: Interactive visualizations
- Pandas & NumPy: Data processing
- OpenAI: Natural language processing

## License
This project is proprietary and confidential. 