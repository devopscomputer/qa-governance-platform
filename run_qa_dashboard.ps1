Clear-Host
Write-Host "===============================" -ForegroundColor Cyan
Write-Host "   QA GOVERNANCE PLATFORM CI   " -ForegroundColor Yellow
Write-Host "===============================" -ForegroundColor Cyan

# Cria pasta de logs
$logDir = "logs"
if (!(Test-Path $logDir)) {
    New-Item -Path $logDir -ItemType Directory | Out-Null
}
$logFile = "$logDir/log_$(Get-Date -Format 'yyyy-MM-dd_HH-mm-ss').txt"

# Etapa 1: Rodar testes
Write-Host "`n▶️  Etapa 1 - Rodando testes..." -ForegroundColor Green
Start-Process powershell -NoNewWindow -Wait -ArgumentList "pytest tests/ --cov=tests --cov-report=xml --alluredir=reports/allure-results | Tee-Object -FilePath $logFile"

# Etapa 2: Gerar métricas
Write-Host "`n📊 Etapa 2 - Gerando métricas..." -ForegroundColor Green
python run_all_metrics.py | Tee-Object -Append -FilePath $logFile

# Etapa 3: Iniciar Streamlit
Write-Host "`n🚀 Etapa 3 - Iniciando dashboard..." -ForegroundColor Green
Start-Process powershell -ArgumentList "streamlit run dashboard/app.py"

Write-Host "`n✅ Finalizado. Logs salvos em: $logFile" -ForegroundColor Cyan
