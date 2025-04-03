Clear-Host
$ErrorActionPreference = "Stop"
$timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$logDir = "logs"
$logFile = "$logDir/log_$timestamp.txt"

# Cores
$cyan = "Cyan"
$yellow = "Yellow"
$green = "Green"
$red = "Red"
$blue = "Blue"
$white = "White"

# Cabeçalho visual
Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════╗" -ForegroundColor $cyan
Write-Host "║       🚀 QA GOVERNANCE PLATFORM - EXECUÇÃO CI        ║" -ForegroundColor $yellow
Write-Host "╚══════════════════════════════════════════════════════╝" -ForegroundColor $cyan
Write-Host ""

# Criar pasta de logs se necessário
if (!(Test-Path $logDir)) {
    New-Item -Path $logDir -ItemType Directory | Out-Null
}

# Etapa 1: Executar os testes com cobertura
Write-Host "╔═[🧪 ETAPA 1]══════════════════════════════════════════╗" -ForegroundColor $blue
Write-Host "║ ▶️ Executando testes com cobertura (pytest + allure) ║" -ForegroundColor $white
Write-Host "╚══════════════════════════════════════════════════════╝" -ForegroundColor $blue
try {
    pytest tests/ --cov=tests --cov-report=xml --alluredir=reports/allure-results | Tee-Object -FilePath $logFile
    Write-Host "✅ Testes executados com sucesso." -ForegroundColor $green
} catch {
    Write-Host "❌ ERRO: Falha na execução dos testes!" -ForegroundColor $red
    Write-Host "Logs: $logFile" -ForegroundColor $cyan
    exit 1
}

# Etapa 2: Gerar métricas
Write-Host ""
Write-Host "╔═[📊 ETAPA 2]══════════════════════════════════════════╗" -ForegroundColor $blue
Write-Host "║ 🔎 Gerando métricas de flakiness, histórico e cobertura ║" -ForegroundColor $white
Write-Host "╚══════════════════════════════════════════════════════╝" -ForegroundColor $blue
try {
    python run_all_metrics.py | Tee-Object -Append -FilePath $logFile
    Write-Host "✅ Métricas geradas com sucesso." -ForegroundColor $green
} catch {
    Write-Host "❌ ERRO: Falha ao gerar as métricas!" -ForegroundColor $red
    Write-Host "Logs: $logFile" -ForegroundColor $cyan
    exit 1
}

# Etapa 3: Iniciar dashboard
Write-Host ""
Write-Host "╔═[📈 ETAPA 3]══════════════════════════════════════════╗" -ForegroundColor $blue
Write-Host "║ 🚀 Iniciando o dashboard Streamlit em nova janela     ║" -ForegroundColor $white
Write-Host "╚══════════════════════════════════════════════════════╝" -ForegroundColor $blue
try {
    Start-Process powershell -WindowStyle Normal -ArgumentList "streamlit run dashboard/app.py"
    Write-Host "✅ Dashboard iniciado em nova aba!" -ForegroundColor $green
} catch {
    Write-Host "❌ ERRO: Falha ao iniciar o dashboard." -ForegroundColor $red
    exit 1
}

# Finalização
Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════╗" -ForegroundColor $cyan
Write-Host "║ ✅ EXECUÇÃO FINALIZADA - ACESSE O DASHBOARD E LOGS   ║" -ForegroundColor $green
Write-Host "║    Dashboard: http://localhost:8501                  ║" -ForegroundColor $white
Write-Host "║    Logs salvos em: $logFile                          ║" -ForegroundColor $white
Write-Host "╚══════════════════════════════════════════════════════╝" -ForegroundColor $cyan
