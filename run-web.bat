@echo off
echo Deep Live Cam - Web Interface
echo =============================
echo.
echo Starting web interface with automatic GPU detection...
echo Open your browser and go to: http://127.0.0.1:5000
echo.
echo Note: If you see CPU execution provider instead of GPU,
echo       run 'fix-gpu-setup.bat' to enable GPU acceleration.
echo.
python run_web.py
echo.
pause 