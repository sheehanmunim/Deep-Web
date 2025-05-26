@echo off
echo Installing additional dependencies for Web Interface...
echo.
pip install flask==2.3.3
pip install flask-cors==4.0.0
pip install werkzeug==2.3.7
pip install pyngrok==7.0.5
echo.
echo Web Interface dependencies installed successfully!
echo You can now run: python run_web.py
pause 