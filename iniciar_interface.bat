@echo off
chcp 65001 >nul
title Sistema de Gestão de Estoque com IA

echo ============================================================
echo    SISTEMA DE GESTAO DE ESTOQUE COM IA
echo ============================================================
echo.

REM Verificar se Python está disponível
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python não encontrado!
    echo Por favor, instale Python 3.11 ou superior.
    pause
    exit /b 1
)

REM Ativar ambiente virtual se existir
if exist ".venv\Scripts\activate.bat" (
    echo [OK] Ativando ambiente virtual...
    call .venv\Scripts\activate.bat
)

REM Executar interface
echo [OK] Iniciando interface gráfica...
echo.
python interface.py

if errorlevel 1 (
    echo.
    echo [ERRO] Erro ao executar a interface.
    echo Verifique se todas as dependências estão instaladas.
    pause
)
