@echo off
echo Deep Live Cam - GPU Setup Fix
echo ==============================
echo.
echo This script will fix GPU acceleration issues.
echo It will uninstall CPU-only ONNX Runtime and install GPU version.
echo.
pause
echo.
echo Fixing GPU setup...
python fix_gpu_setup.py
echo.
pause 