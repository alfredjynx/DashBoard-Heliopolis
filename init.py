from dash import Dash, html, dash_table, dcc
import pandas as pd
import plotly.express as px
import requests

# Getting denuncias from localhost and transforming to dataframe
get_denuncias = requests.get("http://localhost:8080/denuncia")
df_denuncias = pd.DataFrame()
if get_denuncias.status_code == 200:
    denuncias = get_denuncias.json()
    denuncias_list = [denuncia for denuncia in denuncias]
    df_denuncias = pd.DataFrame(denuncias_list)

#---------------------------------------------------------------
app = Dash(__name__)

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')
pop = df['pop']
country = df['country']

app.layout = html.Div([
    html.Div(children='Hello World'),
    dash_table.DataTable(data=df.to_dict('records'), page_size=10),
    dcc.Graph(figure=px.histogram(df, x='continent', y='pop', histfunc='avg'))
])

if __name__ == '__main__':
    app.run_server(debug=True)