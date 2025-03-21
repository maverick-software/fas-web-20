@echo off
echo Starting Financial Analysis System v2.0...
echo.

:: Launch backend in a new window
echo Starting backend server...
start "FAS Backend" cmd /c "%~dp0run_backend.bat"

:: Wait a moment for backend to initialize
timeout /t 3 /nobreak > nul

:: Launch frontend in a new window
echo Starting frontend application...
start "FAS Frontend" cmd /c "%~dp0run_frontend.bat"

echo.
echo Both frontend and backend have been launched in separate windows.
echo.
echo - Frontend UI: http://localhost:8501
echo - Backend API: http://localhost:8000
echo - API Documentation: http://localhost:8000/docs
echo.
echo To stop the application, close the respective windows or press Ctrl+C in each window.
echo.

pause 