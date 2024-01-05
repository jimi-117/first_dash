# Prepare environment
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import numpy as np
import plotly.express as px
import pandas as pd
import folium

# Load csv
data = pd.read_csv("first_dash/sources/arbres10percent.csv")

# Data cleaning
def df_cleaning(dataframe):
    cols =[
    # 'IDBASE',
    # 'TYPE EMPLACEMENT',
    'DOMANIALITE',
    # 'ARRONDISSEMENT',
    # 'COMPLEMENT ADRESSE',
    # 'NUMERO',
    # 'LIEU / ADRESSE',
    # 'IDEMPLACEMENT',
    # 'LIBELLE FRANCAIS',
    # 'GENRE',
    # 'ESPECE',
    # 'VARIETE OUCULTIVAR',
    'CIRCONFERENCE (cm)',
    'HAUTEUR (m)',
    'STADE DE DEVELOPPEMENT',
    # 'REMARQUABLE',
    'geo_point_2d'
    ]
    df = dataframe[cols].dropna(subset='STADE DE DEVELOPPEMENT')
    return df

def df_final(dataframe):
    temp_df = df_cleaning(dataframe)
    coords_df = temp_df['geo_point_2d'].str.split(',', expand=True)
    coords_df.columns = ['lat', 'lon']
    temp_df[['lat', 'lon']] = coords_df
    df = temp_df.drop(columns="geo_point_2d")
    return df

df = df_final(data)


# dash

# init
app = dash.Dash(__name__)

# application layout
app.layout = (
    html.Div(children=[
        html.H1(hildren='Degemer Mat !'),
        dcc.Dropdown(
            id='domanialite-dropdown', 
            options=[{'label': i, 'value': i} for i in df['DOMANIALITE'].unique()],
            value='Alignement'
            ),
        dcc.Dropdown(
            id='stade-development-dropdown', 
            options=[{'label': i, 'value': i} for i in df['STADE DE DEVELOPPEMENT'].unique()],
            value='Adulte'
            ),
        dcc.Graph(id='graph')
    ])
)

# callback decolator
@app.callback(
    Output('graph', 'figure'),
    [Input('omanialite-dropdown', 'value'), 
     Input('stade-development-dropdown', 'value')]
           )
def update_graph(domanialite_value, stade_development_value):
    filtered_df = df[(df['DOMANIALITE'] == domanialite_value) &
                     (df['STADE DE DEVELOPPEMENT'] == stade_development_value)]
    
if __name__ == '__main__':
    app.run_server(debug=True)
