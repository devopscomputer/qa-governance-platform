#!/bin/bash

echo "▶️ Instalando dependências..."
pip install -r requirements.txt

echo "🧪 Executando testes com cobertura..."
pytest tests/ --cov=tests --cov-report=xml --alluredir=reports/allure-results

echo "📈 Gerando métricas..."
python metrics/analyze.py
python metrics/coverage_report.py
python metrics/flakiness_tracker.py

echo "✅ Finalizado."
