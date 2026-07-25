
import streamlit as st
import pandas as pd
import plotly.express as px
import sys
from pathlib import Path

# ===============================
# CONFIGURAÇÃO INICIAL
# ===============================
st.set_page_config(page_title="Dashboard Financeiro Familiar", layout="wide")
st.title("📊 Dashboard de Gestão Financeira Familiar")

# ===============================
# FUNÇÃO PARA CARREGAR DADOS
# ===============================
@st.cache_data
def carregar_dados(path):
    df = pd.read_excel(path, engine="openpyxl")
    df["data"] = pd.to_datetime(df["data"], errors="coerce")
    df["ano_mes"] = df["data"].dt.to_period("M").astype(str)
    return df

# ===============================
# OPÇÃO DE UPLOAD OU ARQUIVO VIA ARG
# ===============================
path_padrao = None
if len(sys.argv) > 1 and sys.argv[-1].endswith(".xlsx"):
    path_padrao = Path(sys.argv[-1])

arquivo = st.file_uploader("📂 Envie um Excel categorizado (.xlsx)", type=["xlsx"])

if arquivo:
    df = carregar_dados(arquivo)
elif path_padrao and path_padrao.exists():
    df = carregar_dados(path_padrao)
    st.success(f"📁 Carregado automaticamente: {path_padrao.name}")
else:
    st.warning("Envie um arquivo .xlsx para visualizar o dashboard.")
    st.stop()

# ===============================
# FILTROS
# ===============================
st.sidebar.header("🎛 Filtros")
categorias = st.sidebar.multiselect("Filtrar por categoria", df["categoria"].dropna().unique(), default=df["categoria"].dropna().unique())
meses = st.sidebar.multiselect("Filtrar por mês", df["ano_mes"].dropna().unique(), default=df["ano_mes"].dropna().unique())

bancos = st.sidebar.multiselect("Filtrar por banco", df["banco"].dropna().unique(), default=df["banco"].dropna().unique())
df_filtros = df[df["categoria"].isin(categorias) & df["ano_mes"].isin(meses) & df["banco"].isin(bancos)]


# ===============================
# MÉTRICAS
# ===============================
col1, col2 = st.columns(2)
col1.metric("💰 Total Recebido", f'R$ {df_filtros[df_filtros["valor"] > 0]["valor"].sum():,.2f}')
col2.metric("💸 Total Gasto", f'R$ {df_filtros[df_filtros["valor"] < 0]["valor"].sum():,.2f}')

# ===============================
# GRÁFICOS
# ===============================
st.markdown("### 📅 Evolução do Saldo por Mês")
saldo_mes = df_filtros.groupby("ano_mes")["valor"].sum().reset_index()
fig_linha = px.line(saldo_mes, x="ano_mes", y="valor", markers=True, title="Evolução do Saldo Mensal")
st.plotly_chart(fig_linha, use_container_width=True)

st.markdown("### 📂 Distribuição por Categoria")
resumo_cat = df_filtros.groupby("categoria")["valor"].sum().reset_index().sort_values(by="valor", ascending=False)
resumo_cat["cor"] = resumo_cat["valor"].apply(lambda x: "darkblue" if x >= 0 else "lightcoral")

fig_bar = px.bar(
    resumo_cat,
    x="categoria",
    y="valor",
    title="Total por Categoria",
    text_auto=True,
    color="cor",
    color_discrete_map="identity"
)
fig_bar.update_layout(showlegend=False)
st.plotly_chart(fig_bar, use_container_width=True)

# ===============================
# TABELA
# ===============================
st.markdown("### 📃 Tabela Detalhada")
st.dataframe(df_filtros.sort_values("data", ascending=False), use_container_width=True)
