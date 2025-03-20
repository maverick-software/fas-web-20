# Financial Analysis System v2.0 - Code Index

## Entry Points

### Frontend
- `frontend/app.py`: Main Streamlit application entry point
  - Function: `main()` - Initializes and runs the Streamlit interface

### Backend
- `backend/app/main.py`: FastAPI server entry point
  - Function: `create_app()` - Creates and configures the FastAPI application
  - Function: `startup()` - Handles server startup tasks

## Core Components

### Frontend Components
- `frontend/components/`
  - `upload.py`: File upload interface
  - `visualization.py`: Data visualization components
  - `command.py`: Natural language command processor
  - `table.py`: Interactive data table display

### Backend Components
- `backend/app/routers/`
  - `data.py`: Data processing endpoints
  - `visualization.py`: Visualization generation endpoints
  - `commands.py`: Natural language command processing

### Data Processing
- `backend/src/data/`
  - `processor.py`: Data transformation and cleaning
  - `validator.py`: Input data validation
  - `storage.py`: Data persistence management

### Visualization Engine
- `backend/src/visualization/`
  - `generator.py`: Chart and graph generation
  - `types.py`: Visualization type definitions
  - `styles.py`: Visual styling configurations

## Configuration Files
- `frontend/requirements.txt`: Frontend dependencies
- `backend/requirements.txt`: Backend dependencies
- `setup.bat`: Environment setup script
- `start_frontend.bat`: Frontend server startup
- `start_backend.bat`: Backend server startup

## Documentation
- `frontend/__ai__.md`: Frontend documentation
- `backend/__ai__.md`: Backend documentation
- `_change.logs`: Project change history
- `README.md`: Project overview and setup guide

## Dependencies
### Frontend
- Streamlit v1.22.0
- Plotly v5.13.0
- Pandas v1.3.0
- NumPy v1.21.0
- OpenPyXL v3.0.9

### Backend
- FastAPI v0.68.0
- Uvicorn v0.15.0
- Pandas v1.3.0
- NumPy v1.21.0
- Python-Multipart (latest) 