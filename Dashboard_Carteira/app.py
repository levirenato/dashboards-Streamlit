import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
# Grafico
base = pd.read_csv("Base_db.csv", sep=";")
base_cliente =base.groupby("CLIENTES")["FATURADO"].sum()
vazamento_cliente =base.groupby("CLIENTES")["VAZAMENTO"].sum()
base_PRODUTO =base.groupby("PRODUTO")["FATURADO"].sum()
#Prpduto
fig_produto = px.histogram(base,x = base["PRODUTO"], y=base["FATURADO"], text_auto=True)
fig_produto.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
# Cliente
fig_cliente = px.histogram(base,x = base["CLIENTES"], y=[base["FATURADO"],base["VAZAMENTO"]], text_auto=True)
fig_cliente.update_layout(margin={"r":0,"t":0,"l":0,"b":0})    

#Layout
col1, col2 = st.columns(2,gap="small")

with col1:
    with st.container():
        st.subheader("Faturavél")
        st.metric(label="R$ 347.987,43", value="R$ 265.557,43",delta="-R$ 82.430,00")
with col2:
    with st.container():
        st.subheader("Total faturado")
        st.metric(label="R$ 265.557,43", value="R$ 1.704.123,52",delta=" R$ 1.969.680,95")

st.title("Valor faturavél por Produto")
st.write(fig_produto)
st.title("Valor faturavél por Cliente")
st.write(fig_cliente)

