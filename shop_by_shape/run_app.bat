@echo off
title Shop by Shape & Skin Tone App
echo ===================================================
echo   Shop by Shape & Skin Tone Recommendation Engine  
echo ===================================================
echo.
echo Launching Streamlit Application...
echo.

where py >nul 2>nul
if %ERRORLEVEL% equ 0 (
    py -m streamlit run phase_4_mvp/app.py
) else (
    python -m streamlit run phase_4_mvp/app.py
)

pause
