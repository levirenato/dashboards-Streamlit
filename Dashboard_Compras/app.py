from plotly.subplots import make_subplots
import plotly.express as px
import streamlit as st
import pandas as pd

df = pd.read_csv("base.csv", sep=";",index_col="ID")
df['Valor'] = df['Valor'].str.replace(",",".")
df['Valor'] = df['Valor'].astype(float)

with st.sidebar:
    st.subheader('Filtros:')
    #df_gp = df.groupby("Setor")["Valor"].sum()
    x= list(df["Setor"].drop_duplicates())
    x.insert(0,"Todos")
    filtro_setor = st.selectbox("Escolha um Setor:",x,index=0)

     # Filtra
    if filtro_setor == "Todos":
        df_escolhido = df
    else: df_escolhido = df.query("Setor == '{}'".format(filtro_setor))
    
    y= list(df_escolhido["Tipo_de_custo"].drop_duplicates())
    y.insert(0,"Todos")
    filtro_tipo = st.selectbox("Escolha um Custo:",y,index=0)
    

with st.container():
    # Cards
    col1,col2,col3 = st.columns(3,gap="medium")
    with col1:
        resultado = '{0:,}'.format(round(df_escolhido.Valor.sum(),2)).replace(',','.')
        st.metric(label="Total", value="{} R$".format(resultado))
    with col2:
        top= df_escolhido.Produto.mode().to_string(index=False)
        df_gp = df.groupby("Produto")["Valor"].sum()
        if filtro_setor == "Sopro":           
            gambiarra = "WEGCONTACTOR TRIP CWM18 18A"
            gambiarra_ = 1260
        else:
            gambiarra = top
            gambiarra_ = df_gp.loc[top]
        st.metric(label="{}".format(gambiarra), value="{} R$".format( gambiarra_ ))
    with col3:
        df_gp = df_escolhido.groupby("Produto")["Valor"].sum()
        top_c= '{0:,}'.format(round(df_gp.max(),2)).replace(',','.')
        st.metric(label="{}".format(df_gp.idxmax()), value="{} R$".format(top_c))   
    
    # Grafico 1
    st.subheader("Valor gasto por setor")
    fig_bar = px.histogram(df_escolhido,x="Tipo_de_custo",y="Valor", text_auto='.4s')
    fig_bar.update_layout(font=dict(size=20),plot_bgcolor="rgba(0, 0, 0, 0)",paper_bgcolor="rgba(0, 0, 0, 0)",margin={"r":0,"t":0,"l":0,"b":0})
    st.write(fig_bar)

    # Grafico 2
    st.subheader("Tipo De gasto (R$)")
    
    if filtro_tipo == "Todos":
        df_2 = df_escolhido
    else: df_2 = df_escolhido.query("Tipo_de_custo == '{}'".format(filtro_tipo))
    

    fig_2 = px.histogram(df_2,x="Produto",y="Valor", text_auto='.4s',orientation='v')
    fig_2.update_layout(font=dict(size=20),plot_bgcolor="rgba(0, 0, 0, 0)",paper_bgcolor="rgba(0, 0, 0, 0)",margin={"r":0,"t":0,"l":0,"b":0},xaxis_tickangle=-45)
    st.write(fig_2)
    
    fig_3 = px.pie(df_2, values='Valor', names='Tipo_de_pagamento')
    fig_3.update_layout(font=dict(size=20),plot_bgcolor="rgba(0, 0, 0, 0)",paper_bgcolor="rgba(0, 0, 0, 0)",margin={"r":0,"t":10,"l":0,"b":0})
    
    st.subheader("Tipo de pagamento")
    st.write(fig_3)
    
    
