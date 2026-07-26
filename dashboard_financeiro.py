
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
    df["ano"] = df["data"].dt.year
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

def multiselect_com_todos(label, opcoes):
    opcoes_ordenadas = sorted(opcoes)
    selecionadas = st.sidebar.multiselect(label, ["TODOS"] + opcoes_ordenadas, default=["TODOS"])
    if "TODOS" in selecionadas:
        return opcoes_ordenadas
    return selecionadas

categorias = multiselect_com_todos("Filtrar por categoria", df["categoria"].dropna().unique().tolist())
anos = multiselect_com_todos("Filtrar por ano", df["ano"].dropna().astype(int).unique().tolist())
meses = multiselect_com_todos("Filtrar por mês", df["ano_mes"].dropna().unique().tolist())
bancos = st.sidebar.multiselect("Filtrar por banco", df["banco"].dropna().unique(), default=df["banco"].dropna().unique())

df_filtros = df[
    df["categoria"].isin(categorias)
    & df["ano"].isin(anos)
    & df["ano_mes"].isin(meses)
    & df["banco"].isin(bancos)
]

# ===============================
# MÉTRICAS
# ===============================
col1, col2 = st.columns(2)
col1.metric("💰 Total Recebido", f'R$ {df_filtros[df_filtros["valor"] > 0]["valor"].sum():,.2f}')
col2.metric("💸 Total Gasto", f'R$ {df_filtros[df_filtros["valor"] < 0]["valor"].sum():,.2f}')

# ===============================
# LAYOUT
# ===============================
# Os blocos são reservados aqui na ordem visual desejada (saldo, categoria,
# tabela), mas a tabela é processada primeiro no código para que a
# descrição selecionada já esteja disponível ao montar os gráficos acima.
bloco_saldo = st.container()
bloco_categoria = st.container()
bloco_tabela = st.container()

# Lê o clique mais recente no gráfico de categoria (se houver) antes de
# montar a tabela, que é desenhada acima dele no layout.
categoria_clicada = None
estado_grafico_categoria = st.session_state.get("grafico_categoria")
if estado_grafico_categoria and estado_grafico_categoria.selection.points:
    categoria_clicada = estado_grafico_categoria.selection.points[0].get("x")

df_tabela = df_filtros[df_filtros["categoria"] == categoria_clicada] if categoria_clicada else df_filtros

with bloco_tabela:
    st.markdown("### 📃 Tabela Detalhada")
    legenda_tabela = "Clique numa linha para filtrar os gráficos acima pela mesma descrição. Clique novamente para limpar."
    if categoria_clicada:
        legenda_tabela += f" Filtrado pela categoria selecionada no gráfico: **{categoria_clicada}**."
    st.caption(legenda_tabela)
    tabela = df_tabela.sort_values("data", ascending=False).reset_index(drop=True)
    evento_tabela = st.dataframe(
        tabela,
        use_container_width=True,
        on_select="rerun",
        selection_mode="single-row",
    )

linhas_selecionadas = evento_tabela.selection.rows
if linhas_selecionadas:
    descricao_selecionada = tabela.iloc[linhas_selecionadas[0]]["descricao"]
    df_grafico = df_filtros[df_filtros["descricao"] == descricao_selecionada]
else:
    descricao_selecionada = None
    df_grafico = df_filtros

# ===============================
# GRÁFICOS
# ===============================
with bloco_saldo:
    st.markdown("### 📅 Evolução do Saldo por Mês")
    if descricao_selecionada:
        st.caption(f"🔎 Filtrado pela descrição selecionada: **{descricao_selecionada}**")
    saldo_mes = df_grafico.groupby("ano_mes")["valor"].sum().reset_index()
    fig_linha = px.line(saldo_mes, x="ano_mes", y="valor", markers=True, title="Evolução do Saldo Mensal")
    st.plotly_chart(fig_linha, use_container_width=True)

with bloco_categoria:
    st.markdown("### 📂 Distribuição por Categoria")
    st.caption("Clique numa barra para filtrar a tabela detalhada por essa categoria. Clique novamente para limpar.")
    if descricao_selecionada:
        st.caption(f"🔎 Filtrado pela descrição selecionada: **{descricao_selecionada}**")
    resumo_cat = df_grafico.groupby("categoria")["valor"].sum().reset_index().sort_values(by="valor", ascending=False)
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
    st.plotly_chart(
        fig_bar,
        use_container_width=True,
        key="grafico_categoria",
        on_select="rerun",
        selection_mode="points",
    )
