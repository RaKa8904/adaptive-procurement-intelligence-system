@echo off
cd /d %~dp0
python -m streamlit run app/dashboard.py
pause
