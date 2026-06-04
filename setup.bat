@echo off
chcp 65001 >nul 2>&1
cd /d "%~dp0"

python setup\verificar_ambiente.py
if errorlevel 9009 (
    echo.
    echo  Python nao encontrado.
    echo  Baixe em: https://www.python.org/downloads/
    echo  IMPORTANTE: marque "Add python.exe to PATH" na instalacao.
    echo.
    start https://www.python.org/downloads/
)
pause
