@echo off
echo Starting Financial Analysis System v2.0...
echo.

:: Change to the frontend directory
cd "%~dp0frontend"
echo Changed to frontend directory: %CD%
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

:: Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if %ERRORLEVEL% NEQ 0 (
        echo ERROR: Failed to create virtual environment.
        goto :error
    )
)

:: Check if activate script exists
if not exist "venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment activation script not found.
    echo This could be because the virtual environment was not created correctly.
    goto :error
)

:: Activate the virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to activate virtual environment.
    goto :error
)

:: Verify activation
echo Verifying virtual environment activation...
where python | findstr /i "venv" >nul
if %ERRORLEVEL% NEQ 0 (
    echo WARNING: Virtual environment may not be activated correctly.
    echo Attempting to proceed anyway...
)

:: Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip
if %ERRORLEVEL% NEQ 0 (
    echo WARNING: Failed to upgrade pip. Continuing anyway...
)

:: Install required packages
echo Installing required packages...
pip install streamlit plotly pandas numpy openpyxl
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to install required packages.
    goto :error
)

echo.
echo Starting Streamlit application...
echo.
echo The application will open in your web browser shortly.
echo (If it doesn't open automatically, go to http://localhost:8501)
echo.
echo Press Ctrl+C to stop the application.
echo.

:: Check if app.py exists
if not exist "app.py" (
    echo ERROR: Frontend application file 'app.py' not found.
    goto :error
)

:: Run the Streamlit application
echo Running: streamlit run app.py
streamlit run app.py

goto :end

:error
echo.
echo Failed to start the application. Please check the error messages above.
pause
exit /b 1

:end
echo.
echo Application closed.
pause 