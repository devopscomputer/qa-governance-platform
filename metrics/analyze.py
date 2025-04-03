import os
import json
import pandas as pd
from datetime import datetime

# Diretórios e arquivos
RESULTS_DIR = "reports/allure-results"
OUTPUT_CSV = "metrics/results.csv"
HISTORY_LOG = "metrics/history_log.csv"
METADATA_FILE = "test_metadata.json"

def extract_allure_results():
    results = []
    for file in os.listdir(RESULTS_DIR):
        if file.endswith(".json") and not file.startswith("history"):
            with open(os.path.join(RESULTS_DIR, file), encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    if "status" in data and "name" in data:
                        results.append({
                            "test_id": data.get("name"),
                            "status": data.get("status"),
                            "duration_sec": round(data.get("time", {}).get("duration", 0) / 1000, 2)
                        })
                except json.JSONDecodeError:
                    continue
    return results

def load_metadata():
    if not os.path.exists(METADATA_FILE):
        return pd.DataFrame()
    with open(METADATA_FILE, encoding="utf-8") as f:
        return pd.DataFrame(json.load(f))

def analyze_and_export():
    print("🔍 Analisando resultados de testes...")
    allure_results = extract_allure_results()
    if not allure_results:
        print("❌ Nenhum teste encontrado.")
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df_results = pd.DataFrame(allure_results)
    df_results["timestamp"] = timestamp

    # Merge com os metadados
    metadata_df = load_metadata()
    df_final = pd.merge(df_results, metadata_df, on="test_id", how="left")

    # KPIs
    df_final["success"] = df_final["status"].apply(lambda s: 1 if s == "passed" else 0)
    df_final["skipped"] = df_final["status"].apply(lambda s: 1 if s == "skipped" else 0)
    df_final["failed"] = df_final["status"].apply(lambda s: 1 if s == "failed" else 0)
    df_final["broken"] = df_final["status"].apply(lambda s: 1 if s == "broken" else 0)

    summary = {
        "timestamp": timestamp,
        "total": len(df_final),
        "passed": int(df_final["success"].sum()),
        "failed": int(df_final["failed"].sum()),
        "broken": int(df_final["broken"].sum()),
        "skipped": int(df_final["skipped"].sum()),
        "success_rate": round((df_final["success"].sum() / max(len(df_final), 1)) * 100, 2),
        "duration_sec": round(df_final["duration_sec"].sum(), 2)
    }

    # Salvar CSV resumido e completo
    os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
    pd.DataFrame([summary]).to_csv(OUTPUT_CSV, index=False)
    print(f"✅ KPIs salvos em: {OUTPUT_CSV}")

    # Histórico acumulado (opcional)
    history_df = pd.DataFrame([summary])
    if os.path.exists(HISTORY_LOG):
        existing = pd.read_csv(HISTORY_LOG)
        history_df = pd.concat([existing, history_df], ignore_index=True)
    history_df.to_csv(HISTORY_LOG, index=False)
    print(f"📈 Histórico atualizado em: {HISTORY_LOG}")

    # Também salva o CSV detalhado para filtro no dashboard
    detailed_csv = "metrics/test_results_detailed.csv"
    df_final.to_csv(detailed_csv, index=False)
    print(f"📊 Resultados detalhados exportados em: {detailed_csv}")

if __name__ == "__main__":
    analyze_and_export()
