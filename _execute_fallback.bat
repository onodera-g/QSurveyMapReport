@echo off
REM Fallback batch file to execute Python script
cd /d C:\Users\ku\Desktop\SurveyPlugin
python _create_gps_jpeg.py
if %ERRORLEVEL% NEQ 0 (
    py _create_gps_jpeg.py
)
