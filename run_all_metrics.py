import os
import subprocess

# Diretórios
ALLURE_DIR = "reports/allure-results"
COVERAGE_XML = "coverage.xml"

print("🚀 Iniciando pipeline de métricas QA...\n")

# 1. Executa os testes com cobertura e relatório Allure
print("🧪 Rodando testes com cobertura e Allure...\n")
pytest_cmd = f"pytest tests/ --cov=tests --cov-report=xml --alluredir={ALLURE_DIR}"
os.system(pytest_cmd)

# 2. Gera KPIs e histórico detalhado
print("\n📊 Extraindo métricas Allure e exportando KPIs...")
os.system("python metrics/analyze.py")

# 3. Gera relatório de flakiness
print("\n🔥 Identificando testes flakey...")
os.system("python metrics/flakiness_tracker.py")

# 4. Extrai cobertura a partir do coverage.xml
print("\n🧪 Calculando cobertura com base no coverage.xml...")
os.system("python metrics/coverage_report.py")

# 5. Validação final
print("\n✅ Pipeline de métricas concluído com sucesso!\n")
print("📁 Verifique os arquivos gerados em /metrics:")
print("  - results.csv")
print("  - test_results_detailed.csv")
print("  - flaky_tests.csv")
print("  - coverage_kpis.csv")
print("  - history_log.csv\n")

print("🌐 Agora você pode executar o dashboard com:")
print("   streamlit run dashboard/app.py")
