@echo on
echo Starting Backend Server...
cd "%~dp0backend"

IF NOT EXIST venv\Scripts\activate.bat (
    echo Error: Virtual environment not found in %cd%\venv\Scripts\
    echo Please run setup.bat first
    pause
    exit /b 1
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Verifying FastAPI installation...
python -c "import fastapi; print(f'FastAPI version: {fastapi.__version__}')"
IF %ERRORLEVEL% NEQ 0 (
    echo Error: FastAPI not found. Please run setup.bat first
    pause
    exit /b 1
)

echo Starting FastAPI server on port 8000...
echo Server will be available at http://localhost:8000
echo API documentation will be at http://localhost:8000/docs
uvicorn app.main:app --host localhost --port 8000 --reload

IF %ERRORLEVEL% NEQ 0 (
    echo Error: Failed to start FastAPI server!
    echo Please check if port 8000 is available
    pause
    exit /b 1
)
pause 