# Financial Analysis System v2.0

An AI-powered real-time data visualization and manipulation tool designed for financial analysts and business professionals. This tool enables seamless dataset analysis through natural language commands and interactive visualizations.

## Features
- Upload and process CSV/XLSX files
- Natural language data manipulation
- Real-time interactive visualizations
- Dark mode user interface
- RESTful API backend

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
├── frontend/           # Streamlit user interface
├── backend/           # FastAPI server
├── setup.bat         # Environment setup script
├── start_frontend.bat # Frontend server startup
└── start_backend.bat  # Backend server startup
```

## Documentation
- Frontend Documentation: [frontend/__ai__.md](frontend/__ai__.md)
- Backend Documentation: [backend/__ai__.md](backend/__ai__.md)
- Change Log: [_change.logs](_change.logs)

## API Documentation
Once the backend server is running, access:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Development
For detailed development guidelines and protocols, see:
- `.cursor/rules/protocols/documentation.mdc`
- `.cursor/rules/compliance.mdc`

## License
This project is proprietary and confidential. 