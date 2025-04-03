Clear-Host
$timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$logDir = "logs"
$logFile = "$logDir/log_$timestamp.txt"
$logTestes = "$logDir/log_testes_$timestamp.txt"
$logMetricas = "$logDir/log_metricas_$timestamp.txt"
$reportPath = "$logDir/relatorio_QA_$timestamp.html"

# Validação inicial avançada
$dependencias = @('pytest', 'python', 'streamlit')
foreach ($dep in $dependencias) {
    if (-not (Get-Command $dep -ErrorAction SilentlyContinue)) {
        Write-Host "[ERRO CRÍTICO] Dependência '$dep' não encontrada! Por favor, instale antes de prosseguir." -ForegroundColor Red
        exit 1
    }
}

# Criar pasta de logs
if (!(Test-Path $logDir)) {
    New-Item -Path $logDir -ItemType Directory | Out-Null
    Write-Host "[INFO] Pasta de logs criada: $logDir" -ForegroundColor Cyan
}

# Função de progresso visual avançado
function Show-Progress {
    param (
        [string]$Message = "⏳ Processando",
        [int]$Seconds = 3
    )
    for ($i = 1; $i -le $Seconds; $i++) {
        Write-Host -NoNewline "$Message"
        for ($j = 1; $j -le 10; $j++) {
            Start-Sleep -Milliseconds 100
            Write-Host -NoNewline "."
        }
        Write-Host ""
    }
}

# Banner ASCII avançado
$banner = @"
 ________  ________          _________  _______   ________  ___  ___     
|\   __  \|\   __  \        |\___   ___\\  ___ \ |\   ____\|\  \|\  \    
\ \  \|\  \ \  \|\  \       \|___ \  \_\ \   __/|\ \  \___|\ \  \\\  \   
 \ \  \\\  \ \   __  \           \ \  \ \ \  \_|/_\ \  \    \ \   __  \  
  \ \  \\\  \ \  \ \  \           \ \  \ \ \  \_|\ \ \  \____\ \  \ \  \ 
   \ \_____  \ \__\ \__\           \ \__\ \ \_______\ \_______\ \__\ \__\
    \|___| \__\|__|\|__|            \|__|  \|_______|\|_______|\|__|\|__|
          \|__|                                                           
"@

# Exibir Cabeçalho
Write-Host $banner -ForegroundColor Cyan
Write-Host "╔══════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║ 🚀 QA GOVERNANCE PLATFORM - EXECUÇÃO INTELIGENTE                 ║" -ForegroundColor Cyan
Write-Host "║ Por Paulo Silas de Campos Filho • Versão Avançada CI Shell       ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan

# ETAPA 1 - Testes
Write-Host "`n╔═[🧪 ETAPA 1]═════════════════════════════════════════════════════╗" -ForegroundColor White
Write-Host "║ ▶️ Executando testes com cobertura (pytest + allure)             ║" -ForegroundColor White
Write-Host "╚══════════════════════════════════════════════════════════════════╝" -ForegroundColor White

$startTime = Get-Date
Show-Progress -Message "🔄 Rodando testes" -Seconds 3
try {
    pytest tests/ --cov=tests --cov-report=xml --alluredir=reports/allure-results | Tee-Object -FilePath $logTestes

    $totalTests = (Select-String -Path $logTestes -Pattern "collected (\d+) items").Matches.Groups[1].Value
    $passedTests = (Select-String -Path $logTestes -Pattern "(\d+) passed").Matches.Groups[1].Value
    $failedTests = (Select-String -Path $logTestes -Pattern "(\d+) failed").Matches.Groups[1].Value
    $coveragePercent = ([xml](Get-Content coverage.xml)).coverage.'line-rate' * 100
    $durationTestes = (Get-Date) - $startTime

    Write-Host "[RESULTADO] Total: $totalTests | ✅ Passaram: $passedTests | ❌ Falharam: $failedTests | 🛡️ Cobertura: $([Math]::Round($coveragePercent,2))% em $($durationTestes.TotalSeconds)s" -ForegroundColor Yellow
} catch {
    Write-Host "[ERROR] Falha na execução dos testes! Detalhes: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# ETAPA 2 - Métricas Avançadas
Write-Host "`n╔═[📊 ETAPA 2]═════════════════════════════════════════════════════╗" -ForegroundColor Blue
Write-Host "║ 📈 Gerando métricas detalhadas de flakiness, histórico e cobertura║" -ForegroundColor White
Write-Host "╚══════════════════════════════════════════════════════════════════╝" -ForegroundColor Blue

$startTime = Get-Date
Show-Progress -Message "📊 Processando métricas" -Seconds 2
try {
    python run_all_metrics.py | Tee-Object -FilePath $logMetricas
    $metrics = Get-Content "metrics_summary.json" | ConvertFrom-Json
    $durationMetricas = (Get-Date) - $startTime

    Write-Host "📍 Flakiness: $($metrics.flakiness)% | Histórico: $($metrics.historic_runs) execuções | Cobertura atual: $($metrics.coverage)% em $($durationMetricas.TotalSeconds)s" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Falha ao gerar métricas detalhadas! Detalhes: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# ETAPA 3 - Dashboard
Write-Host "`n╔═[📈 ETAPA 3]═════════════════════════════════════════════════════╗" -ForegroundColor Blue
Write-Host "║ 🚀 Iniciando Dashboard Streamlit                                 ║" -ForegroundColor White
Write-Host "╚══════════════════════════════════════════════════════════════════╝" -ForegroundColor Blue

try {
    Start-Process powershell -ArgumentList "streamlit run dashboard/app.py"
    Show-Progress -Message "🟢 Carregando Dashboard" -Seconds 5
    Invoke-WebRequest "http://localhost:8501" -TimeoutSec 10 | Out-Null
    Write-Host "[SUCCESS] Dashboard validado e acessível: 🌐 http://localhost:8501" -ForegroundColor Green
} catch {
    Write-Host "[ALERTA] Dashboard pode não ter iniciado corretamente." -ForegroundColor Yellow
}

# Som notificação final
[console]::beep(1000,300)

# Relatório HTML (simplificado)
$reportHtml = @"
<html><body><h2>Relatório QA Governance</h2>
<p>Testes: $passedTests✅, $failedTests❌ | Cobertura: $([Math]::Round($coveragePercent,2))%</p>
<p>Flakiness: $($metrics.flakiness)% | Histórico: $($metrics.historic_runs)</p>
<p><a href='http://localhost:8501'>Acesse o Dashboard</a></p></body></html>
"@
$reportHtml | Out-File -Encoding UTF8 $reportPath

# Finalização
Write-Host "`n📑 Relatório HTML completo: $reportPath" -ForegroundColor Cyan
Write-Host "🎉 Execução completa com sucesso! Logs: $logDir" -ForegroundColor Green
