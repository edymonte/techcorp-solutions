@echo off
chcp 65001 >nul 2>&1
cd /d "%~dp0"

echo.
echo  TechCorp Solutions — Atualizacao do Workshop
echo  ─────────────────────────────────────────────
echo.

REM Adiciona o upstream apenas se ainda nao existir (silencia o erro se já existir)
git remote add upstream https://github.com/edymonte/techcorp-solutions.git 2>nul

REM Baixa as atualizacoes do repositorio original
echo  Buscando atualizacoes...
git fetch upstream >nul 2>&1
if errorlevel 1 (
    echo  ERRO: nao foi possivel conectar ao repositorio.
    echo  Verifique sua conexao com a internet e tente novamente.
    pause
    exit /b 1
)

REM Atualiza apenas o gerador de evidencias (nao toca nos arquivos de exercicio)
echo  Atualizando gerador de evidencias...
git checkout upstream/main -- setup/gerar_evidencia.py
if errorlevel 1 (
    echo  ERRO: falha ao atualizar o arquivo.
    pause
    exit /b 1
)

echo.
echo  Pronto! Atualizacao concluida.
echo.
echo  O que mudou:
echo    - Gerador de evidencias agora e individual (sem --parceiro)
echo    - Numeracao corrigida: --semana 1, 2 e 3
echo.
pause
