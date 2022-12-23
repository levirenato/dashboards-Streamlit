import pandas as pd
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go


#converter = pd.read_excel("Grafico forecast.xlsx", sheet_name=0)
#converter.to_csv('base.csv',sep=';', index=False)
#convr = pd.read_excel("Grafico forecast.xlsx", sheet_name=1)
#convr.to_csv('base_geral.csv',sep=';', index=False)

df = pd.read_csv("base.csv",sep=";")
df_geral = pd.read_csv("base_geral.csv",sep=";")

itens = df['Tipo_Prod'].drop_duplicates()

lista_volume={'ALÇA - 5 LITROS - DIVERSOS':2000,
                  'TAMPA - 5 LITROS - DIVERSOS':2000,
                  'PRE-FORMA 15,7G - DIVERSOS':24360,
                  'PRE-FORMA 83G - DIVERSOS':3200,
                  'TAMPA P/ GARRAFÃO - 10/20L -DIVERSOS':2000}

app = Dash(__name__,external_stylesheets=[dbc.themes.LUX])

server = app.server

app.layout = html.Div([
   dbc.NavbarSimple([
    html.Div([
        dbc.RadioItems(
            id = 'semana',
            options=[
                {"label":"1ª Semana", "value":"1ª SEMANA"},
                {"label":"2ª Semana", "value":"2ª SEMANA"},
                {"label":"Todas", "value":"TODOS"},
            ], value="TODOS", style={"display":"flex","align-self":"center", "margin-left":"1%"}
        ),
        dcc.Dropdown([i for i in itens], [i for i in itens][0], id="produto-escolhido",clearable=False)],style={"width":"400px"}),
   ], brand = "Apontamentos"),

   dbc.Row([
    dbc.Col([
    dbc.Card(
            [
                html.H4("Valor Das Vendas", className="card-title"),
                html.P("", className="card-text", id="vendas-valor", style={"color":"green"}),
                html.P("", className="card-text", id="lucro-valor" )
            ],style={"text-align":"center"},outline=True
        )]),

    dbc.Col([
    dbc.Card(
            [
                html.H4("Unidades Vendidas", className="card-title"),
                html.P("", className="card-text", id="valor-unidade"),
                html.P("", className="card-text", id="valor-volume")
            ],style={"text-align":"center"},outline=True
        )]),
    
    dbc.Col([
    dbc.Card(
            [
                html.H4("Margem de Lucro", className="card-title"),
                html.P("", className="card-text",id="margem_percen-valor"),
                html.P("", className="card-text",id="margem_mone-valor")
            ],style={"text-align":"center","display":"flex"},outline=True
        )]),

   ], style={"margin-top":"1%"}),

    dcc.Graph(
        id='graph',
    )
])


@app.callback(
    Output("graph","figure"),
    [Input("produto-escolhido","value"),Input("semana","value")]
)
def grafico(produto,semana):
    if semana in df['Data'].values:
        periodo = df.query("Data == '{}' and Tipo_Prod =='{}'".format(semana,produto))
    else: periodo = df.query("Tipo_Prod =='{}'".format(produto))

    fig = px.bar(periodo,
    x='Cliente', y='MARGEM R$',color='MARGEM %', color_continuous_scale='rdylgn', text_auto='.4s',title="Resumo por Clientes",
    labels={"VALOR DA VENDA":True})
    fig.update_layout(paper_bgcolor="rgb(0,0,0,0)",plot_bgcolor='rgb(0,0,0,0)')
    return fig

@app.callback(
    Output("vendas-valor","children"),
    Output("lucro-valor","children"),
    Output("valor-unidade","children"),
    Output("valor-volume","children"),
    Output("margem_percen-valor","children"),
    Output("margem_mone-valor","children"),
    [Input("semana","value"),Input("produto-escolhido","value")]
)
def cards(periodo,valor):
    if periodo in df_geral['PERIODO'].values:
        df_g= df_geral.query("PERIODO == '{}'".format(periodo))
    else: df_g = df_geral
    
    # Card 1
    c = float(df_g.query("PRODUTO =='{}'".format(valor))["VALOR DA VENDA"])
    d = float(df_g.query("PRODUTO =='{}'".format(valor))["MARGEM %"])
    vendas_valor= '{}R$'.format(round(c,3))
    lucro_valor = '{}R$'.format(round(d*c,3))
    
    # Card 2
    valor_unidade = '{} Und'.format(int(df_g.query("PRODUTO =='{}'".format(valor))["QUANTIDADE"]))
    valor_volume = '{} Volumes'.format(int(int(df_g.query("PRODUTO =='{}'".format(valor))["QUANTIDADE"])/lista_volume.get(valor))) if valor in lista_volume else '----'
    
    # Card 3
    margem_percent = '{} R$'.format(int(df_g.query("PRODUTO =='{}'".format(valor))["MARGEM R$"]))
    perct = float(df_g.query("PRODUTO =='{}'".format(valor))["MARGEM %"])*100
    margem_cash = '{} %'.format(round(perct,2))
    
    return (vendas_valor,
            lucro_valor,
            valor_unidade,
            valor_volume,
            margem_percent,
            margem_cash
    )



if __name__ == '__main__':
    app.run_server(debug=True)

