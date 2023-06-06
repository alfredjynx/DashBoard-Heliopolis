from dash import Dash, html, dash_table, dcc
import pandas as pd
import plotly.express as px
import requests

# Getting denuncias from localhost and transforming to dataframe
get_denuncias = requests.get("https://3618-186-232-61-4.ngrok-free.app/denuncia")
#---------------------------------------------------------------
app = Dash(__name__)

df = pd.DataFrame(get_denuncias.json())

app.layout = html.Div([
    html.Div([
        html.P('Dash converts Python classes into HTML'),
        html.P("This conversion happens behind the scenes by Dash's JavaScript front-end")
        ], style={"padding": 100, "color": "white", "background-color": "black"}),
    dcc.Graph(figure=px.histogram(df, x='dataDenuncia', title="Denúncias por Data").update_layout(xaxis_title="Data", yaxis_title="Número de Denúncias"), style={"padding": "0.1%", "background-color": "#9a9c9a"}),
    dcc.Graph(figure=px.histogram(df, x='local', title="Denúncias por Local").update_layout(xaxis_title="local", yaxis_title="Número de Denúncias"), style={"padding": "0.1%", "background-color": "#9a9c9a"}),
    dcc.Graph(figure=px.pie(df, names='local', title='Population of European continent'))
], style={'padding':0, "margin":0})

if __name__ == '__main__':
    app.run_server(debug=True)