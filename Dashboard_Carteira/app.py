import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
# Grafico
base = pd.read_csv("Base_db.csv", sep=";")
base_cliente =base.groupby("CLIENTES")["FATURADO"].sum()
base_PRODUTO =base.groupby("PRODUTO")["FATURADO"].sum()
#Prpduto
fig_produto = go.Figure()
fig_produto.add_trace(go.Histogram(x = base_PRODUTO,y = base_PRODUTO.values,text=base_PRODUTO.values,textposition="outside"))
fig_produto.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
# Cliente
fig_cliente = go.Figure()
fig_cliente.add_trace(go.Histogram(x = base_cliente,y = base_cliente.values, name="Faturavél", text=base_cliente.values,textposition="outside"))
fig_cliente.add_trace(go.Histogram(x = base_cliente,y = -base_cliente.values, name="Vazamento",marker_color="red"))
fig_cliente.update_layout(margin={"r":0,"t":0,"l":0,"b":0})


#Layout
col1, col2 = st.columns(2,gap="small")

with col1:
    with st.container():
        st.subheader("Faturavél")
        st.metric(label="R$ 378.979,23", value="R$ 296.549,23",delta="-R$ 82.430,00")
with col2:
    with st.container():
        st.subheader("Total faturado")
        st.metric(label="R$ 296.549,23", value="R$ 1.505.129,76 ",delta="R$ 1.801.678,99")

st.title("Valor faturavél por Produto")
st.write(fig_produto)
st.title("Valor faturavél por Cliente")
st.write(fig_cliente)