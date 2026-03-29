import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =========================
# CONFIGURAÇÃO DA PÁGINA
# =========================
st.set_page_config(page_title="Dashboard de Vendas", layout="wide")

st.title("📊 Dashboard de Vendas")

# =========================
# CARREGAR DADOS
# =========================
df = pd.read_csv('data/Superstore.csv')

# limpar colunas
df.columns = df.columns.str.strip().str.lower()

# converter data
df['order date'] = pd.to_datetime(df['order date'], dayfirst=True)

# =========================
# FILTROS (SIDEBAR)
# =========================
st.sidebar.header("🔎 Filtros")

regiao = st.sidebar.selectbox(
    "Região",
    df['region'].unique()
)

categoria = st.sidebar.multiselect(
    "Categoria",
    df['category'].unique(),
    default=df['category'].unique()
)

data_inicio = st.sidebar.date_input(
    "Data inicial",
    df['order date'].min()
)

data_fim = st.sidebar.date_input(
    "Data final",
    df['order date'].max()
)

# =========================
# FILTRAR DADOS
# =========================
df_filtrado = df[
    (df['region'] == regiao) &
    (df['category'].isin(categoria)) &
    (df['order date'] >= pd.to_datetime(data_inicio)) &
    (df['order date'] <= pd.to_datetime(data_fim))
].copy()

# =========================
# KPIs
# =========================
st.subheader("📌 Indicadores")

col1, col2 = st.columns(2)

faturamento = df_filtrado['sales'].sum()
media_venda = df_filtrado['sales'].mean()

col1.metric("💰 Faturamento Total", f"${faturamento:,.2f}")
col2.metric("📊 Média por Venda", f"${media_venda:,.2f}")

# =========================
# GRÁFICO TEMPORAL
# =========================
st.subheader("📈 Evolução das Vendas")

df_filtrado['mes'] = df_filtrado['order date'].dt.to_period('M')

vendas_mes = df_filtrado.groupby('mes')['sales'].sum()
vendas_mes.index = vendas_mes.index.to_timestamp()

sns.set(style="whitegrid")

fig, ax = plt.subplots(figsize=(10,4))
sns.lineplot(x=vendas_mes.index, y=vendas_mes.values, ax=ax)

ax.set_title('Vendas ao longo do tempo')
ax.set_xlabel('')
ax.set_ylabel('Vendas')

plt.xticks(rotation=45)
st.pyplot(fig)

# =========================
# GRÁFICO POR CATEGORIA
# =========================
st.subheader("📊 Vendas por Categoria")

cat = df_filtrado.groupby('category')['sales'].sum().sort_values()

fig2, ax2 = plt.subplots(figsize=(6,4))
cat.plot(kind='barh', ax=ax2)

ax2.set_title('Vendas por Categoria')

st.pyplot(fig2)

# =========================
# TOP PRODUTOS
# =========================
st.subheader("🏆 Top 10 Produtos")

top_produtos = df_filtrado.groupby('product name')['sales'].sum().sort_values(ascending=False).head(10)

fig3, ax3 = plt.subplots(figsize=(6,4))
top_produtos.sort_values().plot(kind='barh', ax=ax3)

ax3.set_title('Top 10 Produtos')

st.pyplot(fig3)

# =========================
# TABELA DE DADOS
# =========================
st.subheader("📋 Dados Filtrados")

st.dataframe(df_filtrado)