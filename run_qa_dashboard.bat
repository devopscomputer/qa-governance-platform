@echo off
echo ==============================
echo  QA GOVERNANCE PLATFORM - CI
echo ==============================

:: Etapa 1 - Executar os testes com cobertura
echo.
echo ▶️  Rodando testes com cobertura...
pytest tests/ --cov=tests --cov-report=xml --alluredir=reports/allure-results

:: Etapa 2 - Gerar métricas
echo.
echo 📊  Gerando métricas...
python run_all_metrics.py

:: Etapa 3 - Iniciar o dashboard Streamlit
echo.
echo 🚀  Iniciando o dashboard...
streamlit run dashboard/app.py

pause
