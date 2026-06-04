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
echo  [ 1 / 4 ]  Python...
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
echo  [ 2 / 4 ]  Pacotes do projeto...
python -m pip install -r requirements.txt -r requirements-dev.txt --quiet 2>nul
if errorlevel 1 (
    echo  ✘  Falha ao instalar pacotes. Tente rodar o script novamente.
    pause
    exit /b 1
)
echo  ✔  Pacotes instalados

:: ──────────────────────────────────────────────────
echo.
echo  [ 3 / 4 ]  Banco de dados...
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

:: ──────────────────────────────────────────────────
echo.
echo  [ 4 / 4 ]  Ollama e AnythingLLM ^(via Docker^)...

docker info >nul 2>&1
if errorlevel 1 (
    echo.
    echo  ✘  Docker Desktop nao esta em execucao.
    echo.
    echo  O que fazer agora:
    echo    - Se ainda nao instalou: vamos abrir a pagina de download...
    echo    - Se ja instalou: abra o Docker Desktop pelo menu Iniciar
    echo      e aguarde a baleia aparecer na barra de tarefas
    echo    - Depois, execute este script novamente
    echo.
    docker --version >nul 2>&1
    if errorlevel 1 start https://www.docker.com/products/docker-desktop/
    pause
    goto :resultado
)

echo  ✔  Docker esta rodando
echo.
echo     Iniciando containers ^(primeira vez: ~5 min de download^)...
docker compose up -d >nul 2>&1

echo     Aguardando Ollama ficar pronto...
set /a TENTATIVAS=0
:aguarda_ollama
set /a TENTATIVAS+=1
if %TENTATIVAS% gtr 30 goto :ollama_timeout
timeout /t 2 /nobreak >nul
powershell -NoProfile -Command "try{Invoke-WebRequest http://localhost:11434 -TimeoutSec 1 -UseBasicParsing|Out-Null;exit 0}catch{exit 1}" >nul 2>&1
if errorlevel 1 goto :aguarda_ollama

echo     Verificando modelo de IA ^(llama3.2^)...
docker exec techcorp-ollama ollama list 2>nul | findstr /i "llama3.2" >nul
if errorlevel 1 (
    echo     Baixando modelo llama3.2 ^(~2 GB — so na primeira vez^)...
    docker exec techcorp-ollama ollama pull llama3.2
)
echo  ✔  Ollama e AnythingLLM prontos
goto :resultado

:ollama_timeout
echo  ⚠  Ollama ainda esta inicializando. Aguarde 1 minuto e rode:
echo     python setup\verificar_ambiente.py

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
