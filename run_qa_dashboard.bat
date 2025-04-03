@echo off
chcp 65001 > nul
cls
color 0A

:: =====================[ VARIÁVEIS E PREPARAÇÃO ]======================
set LOGDIR=logs
:: Corrigido: gerar nome de log seguro (sem ":" ou "/")
set hour=%time:~0,2%
if "%hour:~0,1%"==" " set hour=0%hour:~1,1%
set minute=%time:~3,2%
set second=%time:~6,2%
for /f "tokens=1-3 delims=/" %%a in ("%date%") do set logdate=%%c-%%a-%%b
set LOGFILE=%LOGDIR%\log_%logdate%_%hour%%minute%%second%.txt


if not exist %LOGDIR% (
    mkdir %LOGDIR%
)

:: =====================[ CABEÇALHO ]===================================
echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║       🚀 QA GOVERNANCE PLATFORM - EXECUÇÃO INTELIGENTE           ║
echo ║           Por Paulo Silas · Versão Avançada CI Shell            ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.

timeout /t 1 > nul
echo ⏳ Preparando ambiente...

:: Verifica dependências essenciais
where python >nul 2>nul || (
    color 0C
    echo ❌ Python não encontrado no PATH. Verifique sua instalação.
    goto FIM
)

where pytest >nul 2>nul || (
    color 0C
    echo ❌ Pytest não encontrado. Instale com: pip install pytest
    goto FIM
)

where streamlit >nul 2>nul || (
    color 0C
    echo ❌ Streamlit não encontrado. Instale com: pip install streamlit
    goto FIM
)

:: =====================[ ETAPA 1: TESTES ]=============================
echo.
echo ╔═[🧪 ETAPA 1]═════════════════════════════════════════════════════╗
echo ║ ▶️ Executando testes com cobertura (pytest + allure)            ║
echo ╚═════════════════════════════════════════════════════════════════╝
echo 📍 Log sendo salvo em: %LOGFILE%
echo.

pytest tests/ --cov=tests --cov-report=xml --alluredir=reports/allure-results >> %LOGFILE% 2>&1
if errorlevel 1 (
    color 0C
    echo ❌ ERRO: Testes falharam. Verifique o log em: %LOGFILE%
    goto FIM
) else (
    echo ✅ Testes executados com sucesso. ✔️
)

:: =====================[ ETAPA 2: MÉTRICAS ]===========================
echo.
echo ╔═[📊 ETAPA 2]═════════════════════════════════════════════════════╗
echo ║ 🔍 Gerando métricas com base nos resultados (.csv automáticos)  ║
echo ╚═════════════════════════════════════════════════════════════════╝
python run_all_metrics.py >> %LOGFILE% 2>&1
if errorlevel 1 (
    color 0C
    echo ❌ ERRO: Falha ao gerar métricas. Veja: %LOGFILE%
    goto FIM
) else (
    echo ✅ Métricas criadas com sucesso em \metrics 📈
)

:: =====================[ ETAPA 3: DASHBOARD ]==========================
echo.
echo ╔═[📈 ETAPA 3]═════════════════════════════════════════════════════╗
echo ║ 🚀 Lançando Dashboard Interativo (Streamlit) em nova janela      ║
echo ╚═════════════════════════════════════════════════════════════════╝
start cmd /k "streamlit run dashboard/app.py"
if errorlevel 1 (
    color 0C
    echo ❌ ERRO: Streamlit não foi iniciado corretamente!
    goto FIM
) else (
    echo ✅ Dashboard iniciado com sucesso no navegador 🧠
)

:: =====================[ FIM ]=========================================
:FIM
color 0B
echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║        ✅ EXECUÇÃO FINALIZADA COM SUCESSO - QA GOVERNANCE        ║
echo ║    Consulte os dados visuais no navegador e os logs em /logs     ║
echo ║          Dashboard: http://localhost:8501                        ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.
:: Emite beep para alertar finalização (som)
echo ^G
pause
