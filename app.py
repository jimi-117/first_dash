import dash
import pandas as pd
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Load and clean the data
def load_and_clean_data(filepath):
    cols_to_use = [
        'DOMANIALITE', 'CIRCONFERENCE (cm)', 'HAUTEUR (m)',
        'STADE DE DEVELOPPEMENT', 'geo_point_2d'
    ]
    df = pd.read_csv(filepath, usecols=cols_to_use).dropna(subset=['STADE DE DEVELOPPEMENT'])
    
    coords = df['geo_point_2d'].str.split(',', expand=True)
    coords.columns = ['lat', 'lon']
    df[['lat', 'lon']] = coords.astype(float)
    
    return df.drop(columns='geo_point_2d')

df = load_and_clean_data("first_dash/sources/arbres10percent.csv")

# Initialize the Dash app

app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div(style={'textAlign': 'center'},children=[
    html.H1(children='Degemer Mat !', style={'textAlign': 'center'}),
    
    dcc.Dropdown(
        id='domanialite-dropdown', 
        options=[{'label': i, 'value': i} for i in df['DOMANIALITE'].unique()],
        value='Alignement',
        style={
            'width': '50%',
            'display' : 'inline-block',
        }
    ),
    dcc.Dropdown(
        id='stade-development-dropdown', 
        options=[{'label': i, 'value': i} for i in df['STADE DE DEVELOPPEMENT'].unique()],
        value='Adulte',
        style={
            'width': '50%',
            'display' : 'inline-block'
        }
    ),
    html.Div(
        style={'width':'45%', 'display':'inline-block'},
        children=[dcc.Graph(id='height-histogram')]
    ),
    html.Div(
        style={'width':'45%', 'display':'inline-block'},
        children=[dcc.Graph(id='circumference-histogram')]
    ),
    html.Div(
        style={'width':'55%','display':'inline-block'},
        children=[dcc.Graph(id='paris-map')]
    )    
])

@app.callback(
    [Output('height-histogram', 'figure'),
     Output('circumference-histogram', 'figure'),
     Output('paris-map', 'figure')],
    [Input('domanialite-dropdown', 'value'), 
     Input('stade-development-dropdown', 'value')]
)
def update_graphs(domanialite_value, stade_development_value):
    if not domanialite_value or not stade_development_value:
        raise PreventUpdate
    
    filtered_df = df[(df['DOMANIALITE'] == domanialite_value) & (df['STADE DE DEVELOPPEMENT'] == stade_development_value)]
    
    height_histogram = px.histogram(filtered_df, x='HAUTEUR (m)', title='Height Distribution')
    circumference_histogram = px.histogram(filtered_df, x='CIRCONFERENCE (cm)', title='Circumference Distribution')

    paris_map = px.scatter_mapbox(
        filtered_df,
        lat='lat',
        lon='lon',
        hover_name='DOMANIALITE',
        hover_data=['STADE DE DEVELOPPEMENT'],
        size_max=15,
        opacity=0.6,
        center={'lat': 48.8566, 'lon': 2.3522},
        zoom=11,
        height=600
    )

    paris_map.update_layout(mapbox_style='open-street-map')
    paris_map.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return height_histogram, circumference_histogram, paris_map

if __name__ == '__main__':
    app.run_server(debug=True)
