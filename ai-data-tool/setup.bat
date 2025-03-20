@echo on
echo Setting up development environment...

echo.
echo Setting up Frontend...
cd "%~dp0frontend"
echo Creating frontend virtual environment...
python -m venv venv
echo Activating frontend virtual environment...
call venv\Scripts\activate.bat
echo Installing frontend dependencies...
python -m pip install --upgrade pip
pip install streamlit==1.22.0
pip install plotly==5.13.0
pip install pandas==1.3.0
pip install numpy==1.21.0
pip install openpyxl==3.0.9

echo.
echo Setting up Backend...
cd "%~dp0backend"
echo Creating backend virtual environment...
python -m venv venv
echo Activating backend virtual environment...
call venv\Scripts\activate.bat
echo Installing backend dependencies...
python -m pip install --upgrade pip
pip install fastapi==0.68.0
pip install uvicorn==0.15.0
pip install pandas==1.3.0
pip install numpy==1.21.0
pip install python-multipart

echo.
echo Setup completed successfully!
echo You can now run start_frontend.bat and start_backend.bat
pause 