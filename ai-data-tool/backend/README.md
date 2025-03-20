# Financial Analysis System Backend

This is the backend component of the Financial Analysis System v2.0. It provides APIs for data analysis and visualization.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- Windows:
```bash
.\venv\Scripts\activate
```
- Unix/MacOS:
```bash
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

To run the application in development mode:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the application is running, you can access:
- Interactive API documentation (Swagger UI): `http://localhost:8000/docs`
- Alternative API documentation (ReDoc): `http://localhost:8000/redoc`

## Project Structure

```
backend/
├── app/
│   ├── api/            # API utilities and dependencies
│   ├── routers/        # API route handlers
│   └── main.py        # FastAPI application initialization
├── src/
│   ├── data/          # Data processing modules
│   └── visualization/ # Visualization generation modules
├── requirements.txt   # Project dependencies
└── README.md         # This file
```

## Available Endpoints

### Data Operations
- `GET /api/data/` - List available data sources and datasets
- `GET /api/data/{dataset_name}` - Retrieve specific dataset

### Visualization Operations
- `GET /api/visualization/types` - List available visualization types
- `POST /api/visualization/generate` - Generate visualization 