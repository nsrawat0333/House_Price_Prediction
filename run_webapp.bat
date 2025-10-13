@echo off
echo Starting House Price Prediction Web Application...
echo.
cd %~dp0
python -m webapp.app
pause