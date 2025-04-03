import os
import xml.etree.ElementTree as ET
import pandas as pd
from datetime import datetime

COVERAGE_XML = "coverage.xml"
OUTPUT_CSV = "metrics/coverage_kpis.csv"

def extract_coverage():
    if not os.path.exists(COVERAGE_XML):
        print("❌ Arquivo coverage.xml não encontrado. Rode: pytest --cov=tests --cov-report=xml")
        return

    try:
        tree = ET.parse(COVERAGE_XML)
        root = tree.getroot()
        coverage_attr = root.attrib.get("line-rate")

        if coverage_attr is None:
            print("⚠️ Atributo 'line-rate' não encontrado no XML.")
            return

        # Convertendo para percentual
        coverage_percent = round(float(coverage_attr) * 100, 2)

        metrics = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "coverage_percent": coverage_percent
        }

        df = pd.DataFrame([metrics])
        os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)

        # Salva novo ou faz append
        if os.path.exists(OUTPUT_CSV):
            existing = pd.read_csv(OUTPUT_CSV)
            df = pd.concat([existing, df], ignore_index=True)

        df.to_csv(OUTPUT_CSV, index=False)
        print(f"✅ Cobertura registrada: {coverage_percent}% → {OUTPUT_CSV}")

        # Alertas
        if coverage_percent < 80:
            print("🚨 ALERTA: cobertura abaixo de 80%!")

    except Exception as e:
        print(f"Erro ao ler coverage.xml: {e}")

if __name__ == "__main__":
    extract_coverage()
