import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
# Grafico
base = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vQwXe7ngD2zNlEJdVw62Oejsb7UbeVlVHgClpceNjZKvpCji3gX8KszbQdgZUKHhCWi5IA2aihV8t_y/pub?gid=0&single=true&output=csv", sep=",")
df_meta = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vQwXe7ngD2zNlEJdVw62Oejsb7UbeVlVHgClpceNjZKvpCji3gX8KszbQdgZUKHhCWi5IA2aihV8t_y/pub?gid=874097056&single=true&output=csv", sep=",")
#Prpduto
fig_produto = px.histogram(base,x = base["PRODUTO"], y=base["FATURAVEL"], text_auto=True)
fig_produto.update_layout(font=dict(size=20),margin={"r":0,"t":0,"l":0,"b":0})
# Cliente
fig_cliente = px.histogram(base,x = base["CLIENTES"], y=[base["FATURAVEL"],base["VAZAMENTO"]], text_auto=True)
fig_cliente.update_layout(margin={"r":0,"t":0,"l":0,"b":0},legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.01),xaxis_range=["YPLASTIC", "LIMPIDA"])  
# MEta
df_injecao = df_meta.query("SETOR == 'INJECAO'")
df_sopro = df_meta.query("SETOR == 'SOPRO'")
 # INJECAO
fig_meta_injecao = px.bar(df_injecao, x="PRODUTO",y=[df_injecao["VALOR ( AC)"],df_injecao["META (R$)"]], text_auto=True)
 # SOPRO
fig_meta_sopro = px.bar(df_sopro, x="PRODUTO",y=[df_sopro["VALOR ( AC)"],df_sopro["META (R$)"]], text_auto=True)
fig_meta_sopro.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.01))  

#Layout
with st.container():
    col1, col2 = st.columns(2,gap="large")

    with col1:
        with st.container():
            st.subheader("Faturavél")
            st.metric(label="R$ 347.987,43", value="R$ 265.557,43",delta="-R$ 82.430,00")
            st.title("Valor faturavél por Cliente")
            st.write(fig_cliente)
            st.title("Faturamento x Meta (Sopro)")
            st.write(fig_meta_sopro)
    with col2:
        with st.container():
            st.subheader("Total faturado")
            st.metric(label="R$ 265.557,43", value="R$ 1.704.123,52",delta=" R$ 1.969.680,95")
            st.title("Valor faturavél por Produto")
            st.write(fig_produto)
            st.title("Faturamento x Meta (Injeção)")
            st.write(fig_meta_injecao)

