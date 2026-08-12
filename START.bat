@echo off
echo ================================
echo   Health A-Z App
echo ================================
python -m venv venv 2>nul
call venv\Scripts\activate
pip install -r requirements.txt -q
echo.
echo Open your browser to: http://localhost:8000/app
echo Press Ctrl+C to stop.
echo.
uvicorn main:app --reload
