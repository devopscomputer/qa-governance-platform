import pandas as pd
import os
import json

# Arquivos
HISTORY_CSV = "metrics/test_results_detailed.csv"
METADATA_JSON = "test_metadata.json"
OUTPUT_CSV = "metrics/flaky_tests.csv"

def load_metadata():
    if not os.path.exists(METADATA_JSON):
        return pd.DataFrame()
    with open(METADATA_JSON, encoding="utf-8") as f:
        return pd.DataFrame(json.load(f))

def track_flaky_tests():
    if not os.path.exists(HISTORY_CSV):
        print(f"❌ Arquivo de histórico '{HISTORY_CSV}' não encontrado.")
        return

    df = pd.read_csv(HISTORY_CSV)
    metadata = load_metadata()

    if "test_id" not in df.columns or "status" not in df.columns:
        print("⚠️ Colunas obrigatórias ausentes: 'test_id' e 'status'.")
        return

    # Agrupa execuções por teste
    grouped = df.groupby("test_id")["status"].nunique().reset_index()

    # Identifica testes flakey (mais de 1 status distinto)
    flaky_tests = grouped[grouped["status"] > 1]["test_id"].tolist()

    # Extrai histórico apenas dos flakey
    flaky_df = df[df["test_id"].isin(flaky_tests)]

    # Estatísticas de falhas/sucessos por teste
    summary = (
        flaky_df.groupby("test_id")["status"]
        .value_counts()
        .unstack(fill_value=0)
        .reset_index()
    )
    summary["execuções"] = summary.sum(axis=1)
    summary["flakiness_rate"] = round(
        summary.get("failed", 0) / summary["execuções"] * 100, 2
    )

    # Enriquecimento com metadados
    enriched = pd.merge(summary, metadata, on="test_id", how="left")

    # Reordena colunas (opcional)
    cols = ["test_id", "type", "priority", "module", "component", "execuções", "flakiness_rate", "passed", "failed", "broken", "skipped", "owner"]
    for col in cols:
        if col not in enriched.columns:
            enriched[col] = "-"
    enriched = enriched[cols]

    # Salva
    os.makedirs("metrics", exist_ok=True)
    enriched.to_csv(OUTPUT_CSV, index=False)
    print(f"✅ Relatório flakey salvo em: {OUTPUT_CSV}")

if __name__ == "__main__":
    track_flaky_tests()
