import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

fig = px.bar(x=[1,5,6,7,8],y=['uva','maçã','banana','pera','jaca'])

base = pd.read_csv("Base_db.csv", sep=";")

st.write( px.histogram(
    base,
    x = base['PRODUTO'],
    y = base['FATURADO']
))