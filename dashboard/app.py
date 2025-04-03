import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Configuração da página
st.set_page_config(page_title="📊 QA Governance Dashboard", layout="wide")
st.title("📊 Plataforma de Governança de Testes")

# Caminhos dos dados
CSV_PATH = "metrics/results.csv"
COVERAGE_PATH = "metrics/coverage_kpis.csv"
FLAKY_PATH = "metrics/flaky_tests.csv"
DETAILED_PATH = "metrics/test_results_detailed.csv"

# Loader com cache
@st.cache_data
def load_data():
    if not os.path.exists(CSV_PATH):
        return None
    df = pd.read_csv(CSV_PATH)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df

@st.cache_data
def load_coverage():
    if os.path.exists(COVERAGE_PATH):
        df = pd.read_csv(COVERAGE_PATH)
        return df.iloc[-1]["coverage_percent"]
    return None

@st.cache_data
def load_detailed():
    if os.path.exists(DETAILED_PATH):
        return pd.read_csv(DETAILED_PATH)
    return pd.DataFrame()

@st.cache_data
def load_flaky():
    if os.path.exists(FLAKY_PATH):
        return pd.read_csv(FLAKY_PATH)
    return pd.DataFrame()

df = load_data()
coverage = load_coverage()
df_detailed = load_detailed()
df_flaky = load_flaky()

if df is None or df.empty:
    st.warning("⚠️ Nenhum dado encontrado. Execute `metrics/analyze.py` após rodar os testes.")
else:
    # 🎯 Filtros interativos
    st.sidebar.header("🔎 Filtros")
    tipo_options = df["type"].dropna().unique().tolist() if "type" in df.columns else []
    status_options = df["status"].dropna().unique().tolist() if "status" in df.columns else []

    tipo_selecionado = st.sidebar.multiselect("Tipo de Teste", tipo_options, default=tipo_options)
    status_selecionado = st.sidebar.multiselect("Status", status_options, default=status_options)

    df_filtrado = df.copy()
    if "type" in df.columns:
        df_filtrado = df_filtrado[df_filtrado["type"].isin(tipo_selecionado)]
    if "status" in df.columns:
        df_filtrado = df_filtrado[df_filtrado["status"].isin(status_selecionado)]

    latest = df_filtrado.iloc[-1] if not df_filtrado.empty else df.iloc[-1]

    # Métrica de cobertura
    if coverage is not None:
        st.metric("🧪 Cobertura (%)", f"{coverage}%")

    # KPIs principais
    st.subheader("🔎 Visão Geral da Última Execução")
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("✅ Passados", int(latest["passed"]))
    col2.metric("❌ Falhos", int(latest["failed"]))
    col3.metric("⚠️ Ignorados", int(latest["skipped"]))
    col4.metric("📉 Sucesso (%)", f"{latest['success_rate']}%")
    col5.metric("⏱️ Duração (s)", f"{latest['duration_sec']}s")

    # Gráfico de linha: evolução
    st.divider()
    st.subheader("📈 Histórico de Execuções")
    st.line_chart(df_filtrado.set_index("timestamp")[["passed", "failed", "broken", "skipped"]])

    # Gráfico de pizza: distribuição atual
    st.subheader("📊 Distribuição de Resultados (última execução)")
    pie_data = {
        "Passados": int(latest["passed"]),
        "Falhos": int(latest["failed"]),
        "Ignorados": int(latest["skipped"]),
        "Quebrados": int(latest["broken"]),
    }
    pie_chart = px.pie(
        names=list(pie_data.keys()),
        values=list(pie_data.values()),
        title="Distribuição dos testes",
        color_discrete_sequence=px.colors.sequential.Tealgrn
    )
    st.plotly_chart(pie_chart, use_container_width=True)

    # 🔥 Flaky tests
    if not df_flaky.empty:
        st.subheader("🔥 Testes Flakey por Prioridade")
        fig_flaky = px.bar(
            df_flaky,
            x="test_id",
            y="flakiness_rate",
            color="priority",
            title="Taxa de Flakiness (%) por Teste",
            labels={"flakiness_rate": "Flakiness (%)", "test_id": "Teste"},
            height=500
        )
        st.plotly_chart(fig_flaky, use_container_width=True)

    # 📊 Gráfico de tipos de teste
    if not df_detailed.empty and "type" in df_detailed.columns:
        st.subheader("📊 Proporção de Tipos de Testes")
        tipo_count = df_detailed["type"].value_counts().reset_index()
        tipo_count.columns = ["type", "total"]
        fig_tipo = px.pie(
            tipo_count,
            names="type",
            values="total",
            title="Proporção de Tipos de Testes",
            color_discrete_sequence=px.colors.sequential.Plasma
        )
        st.plotly_chart(fig_tipo, use_container_width=True)

    # 📦 Status por componente
    if not df_detailed.empty and "component" in df_detailed.columns and "status" in df_detailed.columns:
        st.subheader("📦 Status por Componente")
        comp_data = df_detailed.groupby(["component", "status"]).size().reset_index(name="count")
        fig_comp = px.bar(
            comp_data,
            x="component",
            y="count",
            color="status",
            barmode="group",
            title="Status dos Testes por Componente",
            height=500
        )
        st.plotly_chart(fig_comp, use_container_width=True)

    # 📄 Tabela final
    st.subheader("📄 Histórico Detalhado de Execuções")
    st.dataframe(df_filtrado.sort_values("timestamp", ascending=False), use_container_width=True)
