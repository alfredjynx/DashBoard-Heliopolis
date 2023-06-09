from dash import Dash, html, dash_table, dcc
import pandas as pd
import plotly.express as px
import requests

get_denuncias = requests.get("http://3.23.96.142:8080/denuncia")

df = pd.DataFrame(get_denuncias.json())
df = df.drop(columns=['link','mediaType'])

Mêses = ['Janeiro','Fevereiro','Março','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro']

getMonth = lambda d: Mêses[d.month-1]
getDate = lambda d: d.date()

df['dataEnchente'] = pd.to_datetime((df['dataEnchente']),format='%Y-%m-%d')
df['dataDenuncia'] = pd.to_datetime((df['dataDenuncia']),format='%Y-%m-%d')

df['dataEnchente'] = df['dataEnchente'].apply(getDate)
df['dataDenuncia'] = df['dataDenuncia'].apply(getDate)

df['mesEnchente'] = df['dataEnchente'].apply(getMonth)
df['mesDenuncia'] = df['dataDenuncia'].apply(getMonth)

ultima = df.iloc[len(df)-1]

app = Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.H1('Dash - De Olho na Quebrada', style={'justify-content':'center'}),
        ], style={"padding": '1%', "color": "#f5d4ae", "background-color": "black", 'font-size':'5rem', 'font-weight':'20rem','justify-content':'center'}),
    html.Div([
        html.Div([
            html.H2('Último Relato', style={'display':'flex','justify-content':'center'}),
            html.P('"' + ultima['relato']+'"' +" - " + ultima['nome'],style={'justify-content':'center','display':'flex'})
            ], style={"padding": '1%', "color": "black", "background-color": "#f5d4ae",'display':'flex','flex-direction':'column','height':'10%','width':'50%'}),
        html.Div([
            html.H2('Número Total de Denúncias', style={'display':'flex','justify-content':'center'}),
            html.P(len(df),style={'justify-content':'center','display':'flex'})
            ], style={"padding": '1%', "color": "white", "background-color": "#F4663A",'display':'flex','flex-direction':'column','height':'10%','width':'50%'})
    ],style={'padding':0, 'margin':0,'display':'flex','flex-direction':'row','height':'10%'}),
    dcc.Graph(figure=px.histogram(df, x='dataDenuncia', title="Denúncias por Data").update_layout(xaxis_title="Data", yaxis_title="Número de Denúncias"), style={"padding-bottom": "0.1%", "background-color": "#9a9c9a"}),
    dcc.Graph(figure=px.histogram(df, x='local', title="Denúncias por Região").update_layout(xaxis_title="Região", yaxis_title="Número de Denúncias"), style={"padding-bottom": "0.1%", "background-color": "#9a9c9a"}),
    dcc.Graph(figure=px.histogram(df, x='mesDenuncia', title="Denúncias por Mês").update_layout(xaxis_title="Mês do Ano", yaxis_title="Número de Denúncias"), style={"padding-bottom": "0.1%", "background-color": "#9a9c9a"}),
    dcc.Graph(figure=px.histogram(df, x='mesEnchente', title="Enchentes por Mês").update_layout(xaxis_title="Mês do Ano", yaxis_title="Número de Enchentes Relatadas"), style={"padding-bottom": "0.1%", "background-color": "#9a9c9a"}),
    dcc.Graph(figure=px.pie(df, names='local', title='Porcentagem de Denúncias por Região'),style={"padding-bottom": "0.1%", "background-color": "#9a9c9a"}),
    dcc.Graph(figure=px.pie(df, names='mesDenuncia', title='Porcentagem de Denúncias por Mês'),style={"padding-bottom": "0.1%", "background-color": "#9a9c9a"}),
    dcc.Graph(figure=px.pie(df, names='mesEnchente', title='Porcentagem de Enchente Relatadas por Mês'),style={"padding-bottom": "0.1%", "background-color": "#9a9c9a"})
], style={'padding':0, "margin":0,"font-family": "Open Sans,sans-serif"})

if __name__ == '__main__':
    app.run_server(debug=True)