@echo off
chcp 65001 >nul 2>&1
setlocal enabledelayedexpansion

cd /d "%~dp0"

echo.
echo ████████████████████████████████████████████████████
echo      TechCorp Workshop — Preparando seu ambiente
echo ████████████████████████████████████████████████████
echo.
echo  Isso pode levar alguns minutos na primeira vez.
echo  Pode deixar rodando e tomar um cafe! ☕
echo.

:: ──────────────────────────────────────────────────
echo  [ 1 / 3 ]  Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo  ✘  Python nao encontrado.
    echo.
    echo  O que fazer agora:
    echo    1. Vamos abrir a pagina de download automaticamente...
    echo    2. Baixe e instale o Python 3.11
    echo    3. IMPORTANTE: na primeira tela da instalacao,
    echo       marque a opcao  "Add python.exe to PATH"
    echo    4. Apos instalar, feche e abra este script novamente
    echo.
    start https://www.python.org/downloads/
    pause
    exit /b 1
)
for /f "tokens=2" %%v in ('python --version 2^>^&1') do set PYVER=%%v
echo  ✔  Python %PYVER%

:: ──────────────────────────────────────────────────
echo.
echo  [ 2 / 3 ]  Pacotes do projeto...
python -m pip install -r requirements.txt -r requirements-dev.txt --quiet 2>nul
if errorlevel 1 (
    echo  ✘  Falha ao instalar pacotes. Tente rodar o script novamente.
    pause
    exit /b 1
)
echo  ✔  Pacotes instalados

:: ──────────────────────────────────────────────────
echo.
echo  [ 3 / 3 ]  Banco de dados...
if exist "db\techcorp.db" (
    echo  ✔  Banco de dados ja existe
) else (
    python db\init_db.py >nul 2>&1
    if errorlevel 1 (
        echo  ✘  Erro ao criar o banco. Tente rodar o script novamente.
        pause
        exit /b 1
    )
    echo  ✔  Banco de dados criado
)

:resultado
:: ──────────────────────────────────────────────────
echo.
echo ████████████████████████████████████████████████████
echo      Resultado
echo ████████████████████████████████████████████████████
timeout /t 2 /nobreak >nul
python setup\verificar_ambiente.py
echo.
pause
