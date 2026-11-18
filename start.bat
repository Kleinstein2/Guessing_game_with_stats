@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt --quiet
.venv\Scripts\python.exe -m streamlit run app.py
pause