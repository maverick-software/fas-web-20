@echo on
echo Starting Frontend Server...
cd "%~dp0frontend"

IF NOT EXIST venv\Scripts\activate.bat (
    echo Error: Virtual environment not found in %cd%\venv\Scripts\
    echo Please run setup.bat first
    pause
    exit /b 1
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Verifying Streamlit installation...
streamlit --version
IF %ERRORLEVEL% NEQ 0 (
    echo Error: Streamlit not found. Please run setup.bat first
    pause
    exit /b 1
)

echo Starting Streamlit server on port 8501...
echo Server will be available at http://localhost:8501
streamlit run app.py --server.port 8501 --server.address localhost

IF %ERRORLEVEL% NEQ 0 (
    echo Error: Failed to start Streamlit server!
    echo Please check if port 8501 is available
    pause
    exit /b 1
)
pause 