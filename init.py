from dash import Dash, html, dash_table, dcc
import pandas as pd
import plotly.express as px


app = Dash(__name__)

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

pop = df['pop']
country = df['country']


app.layout = html.Div([
    html.Div(children='Hello World'),
    dash_table.DataTable(data=df.to_dict('records'), page_size=10),
    dcc.Graph(figure=px.histogram(df, x='continent', y='pop',histfunc='avg'))
])

if __name__ == '__main__':
    app.run_server(debug=True)