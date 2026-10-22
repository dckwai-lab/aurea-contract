@echo off
color 0B
echo ===================================================
echo        PROJETO AUREA - DEMO AUTOMATICA
echo ===================================================
echo.
echo [1] Verificando dependencias do Python...
python -m pip install -r requirements.txt >nul 2>&1

echo [2] Executando o Loop Aurea (IA + FHIR + NEAR)...
echo.
python agent.py

echo.
pause