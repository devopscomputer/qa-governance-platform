import streamlit as st
import pandas as pd

st.title("📊 QA Metrics Dashboard")
df = pd.read_csv("metrics/results.csv")
st.metric("Testes Executados", len(df))
st.bar_chart(df['status'].value_counts())
