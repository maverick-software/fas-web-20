# Backend Component Documentation

## Directory Purpose
Houses the FastAPI-based server implementation that handles data processing, AI command interpretation, and visualization generation.

## Structure
- `/app/` - Main application package
  - `main.py` - FastAPI application entry point
  - `/api/` - API utilities and dependencies
  - `/routers/` - API route handlers
- `/src/` - Source code modules
  - `/data/` - Data processing modules
  - `/visualization/` - Visualization generation modules
- `requirements.txt` - Backend dependencies
- `/venv/` - Python virtual environment (created by setup.bat)

## Key Files
- `app/main.py`: FastAPI application initialization and CORS configuration
- `app/routers/data.py`: Data operation endpoints
- `app/routers/visualization.py`: Visualization generation endpoints

## Dependencies
Specific versions used:
- fastapi==0.68.0
- uvicorn==0.15.0
- pandas==1.3.0
- numpy==1.21.0
- python-multipart (latest)

## API Endpoints
- `GET /`: Root endpoint with welcome message
- `GET /api/data/`: List available data sources and datasets
- `GET /api/data/{dataset_name}`: Retrieve specific dataset
- `GET /api/visualization/types`: List available visualization types
- `POST /api/visualization/generate`: Generate visualization

## Server Configuration
- Port: 8000
- Host: localhost
- Documentation URL: http://localhost:8000/docs
- Alternative Documentation: http://localhost:8000/redoc 