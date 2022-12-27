from plotly.subplots import make_subplots
import plotly.graph_objects as go
import streamlit as st
import pandas as pd

df = pd.read_csv("ESTOQUE MÍNINO-MÁXIMO.csv", sep=";")


fig = go.Figure()

prod = st.selectbox('Produto:', [i for i in df["PRODUTO"]])


dff = df.query("PRODUTO == '{}'".format(prod))

fig.add_trace(go.Bar(x=dff["PRODUTO"], y=dff['ATUAL'],name='Estoque Atual',text=dff['ATUAL'],textposition='auto',texttemplate='%{text:.2s}'))
fig.add_trace(go.Bar(x=dff["PRODUTO"], y=dff['MAXIMO'],name='Estoque Máximo',text=dff['MAXIMO'],textposition='auto',texttemplate='%{text:.2s}'))
fig.update_layout(barmode='group',font=dict(size=20))


st.write(fig)