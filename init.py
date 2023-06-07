from dash import Dash, html, dash_table, dcc
import pandas as pd
import plotly.express as px
import requests

get_denuncias = requests.get("http://3.23.96.142:8080/denuncia")

df = pd.DataFrame(get_denuncias.json())
df = df.drop(columns=['link','mediaType'])

getMonth = lambda d: d.month

df['dataEnchente'] = pd.to_datetime((df['dataEnchente']),format='%Y-%m-%d')
df['dataDenuncia'] = pd.to_datetime((df['dataDenuncia']),format='%Y-%m-%d')

df['mesEnchente'] = df['dataEnchente'].apply(getMonth)
df['mesDenuncia'] = df['dataDenuncia'].apply(getMonth)

app = Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.P('Dash converts Python classes into HTML'),
        html.P("This conversion happens behind the scenes by Dash's JavaScript front-end")
        ], style={"padding": 100, "color": "white", "background-color": "black"}),
    dcc.Graph(figure=px.histogram(df, x='dataDenuncia', title="Denúncias por Data").update_layout(xaxis_title="Data", yaxis_title="Número de Denúncias"), style={"padding": "0.1%", "background-color": "#9a9c9a"}),
    dcc.Graph(figure=px.histogram(df, x='local', title="Denúncias por Local").update_layout(xaxis_title="local", yaxis_title="Número de Denúncias"), style={"padding": "0.1%", "background-color": "#9a9c9a"}),
    dcc.Graph(figure=px.histogram(df, x='mesDenuncia', title="Denúncias por Mes").update_layout(xaxis_title="Mês do Ano (número)", yaxis_title="Número de Denúncias"), style={"padding": "0.1%", "background-color": "#9a9c9a"}),
    dcc.Graph(figure=px.histogram(df, x='mesEnchente', title="Enchentes por Mes").update_layout(xaxis_title="Mês do Ano (número)", yaxis_title="Número de Enchentes Relatadas"), style={"padding": "0.1%", "background-color": "#9a9c9a"}),
    dcc.Graph(figure=px.pie(df, names='local', title='Porcentagem de Denúncias por Região'),style={"padding": "0.1%", "background-color": "#9a9c9a"}),
    dcc.Graph(figure=px.pie(df, names='mesDenuncia', title='Porcentagem de Denúncias por Mes'),style={"padding": "0.1%", "background-color": "#9a9c9a"}),
    dcc.Graph(figure=px.pie(df, names='mesEnchente', title='Porcentagem de Enchente Relatadas por Mes'),style={"padding": "0.1%", "background-color": "#9a9c9a"})
], style={'padding':0, "margin":0})

if __name__ == '__main__':
    app.run_server(debug=True)