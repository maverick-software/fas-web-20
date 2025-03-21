@echo off
echo Starting Financial Analysis System v2.0 Backend...
echo.

:: Change to the backend directory
cd backend
echo Changed to backend directory: %CD%
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python is not installed or not in PATH.
    echo Please install Python 3.9+ and try again.
    goto :error
)

echo Setting up environment...
echo.

:: Remove existing virtual environment if it's broken
if exist "venv" (
    echo Removing existing virtual environment...
    rmdir /s /q venv
    if %ERRORLEVEL% NEQ 0 (
        echo WARNING: Could not remove existing virtual environment.
        echo Will attempt to proceed without it.
    )
)

:: Create a fresh virtual environment
echo Creating a fresh virtual environment...
python -m venv venv
if %ERRORLEVEL% NEQ 0 (
    echo WARNING: Failed to create virtual environment.
    echo Will attempt to install packages globally instead.
    goto :skip_venv
)

:: Check if activate script exists
if not exist "venv\Scripts\activate.bat" (
    echo WARNING: Virtual environment activation script not found.
    echo Will attempt to install packages globally instead.
    goto :skip_venv
)

:: Activate the virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
if %ERRORLEVEL% NEQ 0 (
    echo WARNING: Failed to activate virtual environment.
    echo Will attempt to install packages globally instead.
    goto :skip_venv
)

echo Successfully activated virtual environment.
goto :install_packages

:skip_venv
echo Proceeding without virtual environment...

:install_packages
:: Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip
if %ERRORLEVEL% NEQ 0 (
    echo WARNING: Failed to upgrade pip. Continuing anyway...
)

:: Install required packages
echo Installing required packages...
echo fastapi>=0.68.0,<0.69.0 > requirements.txt
echo uvicorn>=0.15.0,<0.16.0 >> requirements.txt
echo pandas>=2.2.0,<2.3.0 >> requirements.txt
echo numpy>=1.24.0,<1.27.0 >> requirements.txt
echo cassandra-driver>=3.25.0,<3.26.0 >> requirements.txt
echo openai>=0.27.0,<0.28.0 >> requirements.txt
echo python-dotenv>=0.19.0,<0.20.0 >> requirements.txt
echo pydantic>=1.8.0,<1.9.0 >> requirements.txt

python -m pip install --only-binary :all: -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to install required packages.
    goto :error
)

echo.
echo Starting FastAPI backend server...
echo.
echo The API will be available at http://localhost:8000
echo API documentation will be available at http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server.
echo.

:: Check if main.py exists
if not exist "app\main.py" (
    echo ERROR: Backend application file 'app\main.py' not found.
    goto :error
)

:: Run the FastAPI application
echo Running: uvicorn app.main:app --reload
uvicorn app.main:app --reload

goto :end

:error
echo.
echo Failed to start the backend server. Please check the error messages above.
pause
exit /b 1

:end
echo.
echo Backend server closed.
pause 