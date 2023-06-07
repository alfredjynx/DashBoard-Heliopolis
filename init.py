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

ultima = df.iloc[len(df)-1]

app = Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.H1('Dash - De Olho na Quebrada', style={'justify-content':'center'}),
        ], style={"padding": '1%', "color": "white", "background-color": "black", 'font-size':'5rem', 'font-weight':'20rem','justify-content':'center'}),
    html.Div([
        html.H2('Último Relato', style={'display':'flex','justify-content':'center'}),
        html.P('"' + ultima['relato']+'"' +" - " + ultima['nome'],style={'justify-content':'center','display':'flex'})
        ], style={"margin": '1%', "color": "black", "background-color": "white",'display':'flex','flex-direction':'column','height':'10%'}),
    dcc.Graph(figure=px.histogram(df, x='dataDenuncia', title="Denúncias por Data").update_layout(xaxis_title="Data", yaxis_title="Número de Denúncias"), style={"padding-bottom": "0.1%", "background-color": "#9a9c9a"}),
    dcc.Graph(figure=px.histogram(df, x='local', title="Denúncias por Local").update_layout(xaxis_title="local", yaxis_title="Número de Denúncias"), style={"padding-bottom": "0.1%", "background-color": "#9a9c9a"}),
    dcc.Graph(figure=px.histogram(df, x='mesDenuncia', title="Denúncias por Mes").update_layout(xaxis_title="Mês do Ano (número)", yaxis_title="Número de Denúncias"), style={"padding-bottom": "0.1%", "background-color": "#9a9c9a"}),
    dcc.Graph(figure=px.histogram(df, x='mesEnchente', title="Enchentes por Mes").update_layout(xaxis_title="Mês do Ano (número)", yaxis_title="Número de Enchentes Relatadas"), style={"padding-bottom": "0.1%", "background-color": "#9a9c9a"}),
    dcc.Graph(figure=px.pie(df, names='local', title='Porcentagem de Denúncias por Região'),style={"padding-bottom": "0.1%", "background-color": "#9a9c9a"}),
    dcc.Graph(figure=px.pie(df, names='mesDenuncia', title='Porcentagem de Denúncias por Mes'),style={"padding-bottom": "0.1%", "background-color": "#9a9c9a"}),
    dcc.Graph(figure=px.pie(df, names='mesEnchente', title='Porcentagem de Enchente Relatadas por Mes'),style={"padding-bottom": "0.1%", "background-color": "#9a9c9a"})
], style={'padding':0, "margin":0,"font-family": "Open Sans,sans-serif"})

if __name__ == '__main__':
    app.run_server(debug=True)