import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# 🌌 Estilo futurista + dark
st.set_page_config(
    page_title="🧠 QA Governance Platform",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🌑 CSS global personalizado
st.markdown("""
    <style>
    /* === ESTILO GERAL === */
    html, body, [class*="css"] {
        background-color: #0f1117;
        color: #ffffff;
        font-family: 'Segoe UI', sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    }

    .block-container {
        background: rgba(255, 255, 255, 0.04);
        border-radius: 18px;
        padding: 2rem;
        box-shadow: 0 0 25px rgba(0, 255, 255, 0.08);
        backdrop-filter: blur(12px);
    }

    section[data-testid="stSidebar"] {
        background-color: rgba(0, 60, 60, 0.15);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(0, 255, 255, 0.1);
    }

    header[data-testid="stHeader"] {
        background: transparent;
    }

    /* === TABELA: remove fundo preto do st.dataframe/ag-grid === */
    [data-testid="stDataFrame"] iframe {
        background-color: transparent !important;
    }

    iframe[title="dataframe"] {
        background: transparent !important;
        border-radius: 12px;
        box-shadow: 0 0 20px rgba(0,255,255,0.04);
    }

    /* Força grid clara por dentro da tabela */
    .stDataFrame {
        background: transparent !important;
    }

    .element-container:has(iframe) {
        background-color: transparent !important;
        padding: 0 !important;
    }
    </style>
""", unsafe_allow_html=True)

# 🧬 Caminhos dos dados
CSV_PATH = "metrics/results.csv"
COVERAGE_PATH = "metrics/coverage_kpis.csv"
FLAKY_PATH = "metrics/flaky_tests.csv"
DETAILED_PATH = "metrics/test_results_detailed.csv"

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

# 🚀 Carregamento dos dados
df = load_data()
coverage = load_coverage()
df_detailed = load_detailed()
df_flaky = load_flaky()

# 🧠 Título
st.title("🧠 Plataforma de Governança de Testes")

if df is None or df.empty:
    st.warning("⚠️ Nenhum dado encontrado. Execute `metrics/analyze.py` após rodar os testes.")
else:
    # 🎛️ Filtros
    st.sidebar.header("🧪 Filtros")
    tipo_options = df["type"].dropna().unique().tolist() if "type" in df.columns else []
    status_options = df["status"].dropna().unique().tolist() if "status" in df.columns else []

    tipo_selecionado = st.sidebar.multiselect("🔬 Tipo de Teste", tipo_options, default=tipo_options)
    status_selecionado = st.sidebar.multiselect("📌 Status", status_options, default=status_options)

    df_filtrado = df.copy()
    if "type" in df.columns:
        df_filtrado = df_filtrado[df_filtrado["type"].isin(tipo_selecionado)]
    if "status" in df.columns:
        df_filtrado = df_filtrado[df_filtrado["status"].isin(status_selecionado)]

    latest = df_filtrado.iloc[-1] if not df_filtrado.empty else df.iloc[-1]

    # ✅ Cobertura
    if coverage is not None:
        st.metric("🧪 Cobertura (%)", f"{coverage}%")

    # KPIs principais
    st.subheader("📊 Visão Geral da Última Execução")
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("✅ Passados", int(latest["passed"]))
    col2.metric("❌ Falhos", int(latest["failed"]))
    col3.metric("⚠️ Ignorados", int(latest["skipped"]))
    col4.metric("📉 Sucesso (%)", f"{latest['success_rate']}%")
    col5.metric("⏱️ Duração (s)", f"{latest['duration_sec']}s")

    st.divider()

    # 📈 Histórico moderno com gradiente
    st.subheader("📈 Histórico de Execuções")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_filtrado['timestamp'], y=df_filtrado['passed'], mode='lines+markers',
        name='✅ Passados', line=dict(color='lime', width=3),
        fill='tozeroy', fillcolor='rgba(0,255,0,0.1)'
    ))
    fig.add_trace(go.Scatter(
        x=df_filtrado['timestamp'], y=df_filtrado['failed'], mode='lines+markers',
        name='❌ Falhos', line=dict(color='red', width=3),
        fill='tozeroy', fillcolor='rgba(255,0,0,0.1)'
    ))
    fig.add_trace(go.Scatter(
        x=df_filtrado['timestamp'], y=df_filtrado['broken'], mode='lines+markers',
        name='⚠️ Quebrados', line=dict(color='orange', width=3),
        fill='tozeroy', fillcolor='rgba(255,165,0,0.1)'
    ))
    fig.add_trace(go.Scatter(
        x=df_filtrado['timestamp'], y=df_filtrado['skipped'], mode='lines+markers',
        name='⏭️ Ignorados', line=dict(color='cyan', width=3),
        fill='tozeroy', fillcolor='rgba(0,255,255,0.1)'
    ))
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_title='Data',
        yaxis_title='Total de Testes',
        hovermode='x unified',
        font=dict(color='white'),
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)

    # 📊 Distribuição de Resultados
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
    pie_chart.update_layout(paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(pie_chart, use_container_width=True)

    # 🔥 Testes flakey
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
        fig_flaky.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_flaky, use_container_width=True)

    # 🧪 Proporção de Tipos
    if not df_detailed.empty and "type" in df_detailed.columns:
        st.subheader("🧪 Proporção de Tipos de Testes")
        tipo_count = df_detailed["type"].value_counts().reset_index()
        tipo_count.columns = ["type", "total"]
        fig_tipo = px.pie(
            tipo_count,
            names="type",
            values="total",
            title="Proporção de Tipos de Testes",
            color_discrete_sequence=px.colors.sequential.Plasma
        )
        fig_tipo.update_layout(paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_tipo, use_container_width=True)

    # 🧩 Status por Componente (sem fundo preto)
    if not df_detailed.empty and "component" in df_detailed.columns and "status" in df_detailed.columns:
        st.subheader("🧩 Status por Componente")
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
        fig_comp.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_comp, use_container_width=True)

    # 📋 Histórico Detalhado
st.subheader("📋 Histórico Detalhado de Execuções")
st.dataframe(
    df_filtrado.sort_values("timestamp", ascending=False),
    height=300,
    use_container_width=True
)
