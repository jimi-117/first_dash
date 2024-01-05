import dash
import pandas as pd
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Function to load and preprocess the dataset
def load_and_clean_data(filepath):
    # Specify the columns to be used
    cols_to_use = [
        'DOMANIALITE', 'CIRCONFERENCE (cm)', 'HAUTEUR (m)',
        'STADE DE DEVELOPPEMENT', 'geo_point_2d'
    ]
    # Read the dataset and drop rows with missing 'STADE DE DEVELOPPEMENT'
    df = pd.read_csv(filepath, usecols=cols_to_use).dropna(subset=['STADE DE DEVELOPPEMENT'])
    
    # Split 'geo_point_2d' into two separate columns for latitude and longitude
    coords = df['geo_point_2d'].str.split(',', expand=True)
    coords.columns = ['lat', 'lon']
    df[['lat', 'lon']] = coords.astype(float)
    
    # Return the DataFrame without the original 'geo_point_2d' column
    return df.drop(columns='geo_point_2d')

# Load the data using the function
df = load_and_clean_data("first_dash/sources/arbres10percent.csv")

# Initialize the Dash application
app = dash.Dash(__name__)

# Define the layout of the application
app.layout = html.Div(style={'textAlign': 'center'}, children=[
    # Application title
    html.H1(children='Degemer Mat !', style={'textAlign': 'center'}),
    
    # Dropdown for 'DOMANIALITE' selection
    dcc.Dropdown(
        id='domanialite-dropdown', 
        options=[{'label': i, 'value': i} for i in df['DOMANIALITE'].unique()],
        value='Alignement',
        style={'width': '50%', 'display': 'inline-block'},
    ),
    # Dropdown for 'STADE DE DEVELOPPEMENT' selection
    dcc.Dropdown(
        id='stade-development-dropdown', 
        options=[{'label': i, 'value': i} for i in df['STADE DE DEVELOPPEMENT'].unique()],
        value='Adulte',
        style={'width': '50%', 'display': 'inline-block'}
    ),
    # Graph container for the height histogram
    html.Div(
        style={'width': '45%', 'display': 'inline-block'},
        children=[dcc.Graph(id='height-histogram')]
    ),
    # Graph container for the circumference histogram
    html.Div(
        style={'width': '45%', 'display': 'inline-block'},
        children=[dcc.Graph(id='circumference-histogram')]
    ),
    # Graph container for the Paris map visualization
    html.Div(
        style={'width': '55%', 'display': 'inline-block'},
        children=[dcc.Graph(id='paris-map')]
    )    
])

# Callback to update the graphs based on the dropdown selections
@app.callback(
    [Output('height-histogram', 'figure'),
     Output('circumference-histogram', 'figure'),
     Output('paris-map', 'figure')],
    [Input('domanialite-dropdown', 'value'),
     Input('stade-development-dropdown', 'value')]
)
def update_graphs(domanialite_value, stade_development_value):
    # Prevent update if dropdown has no value
    if not domanialite_value or not stade_development_value:
        raise PreventUpdate
    
    # Filter the DataFrame based on dropdown selections
    filtered_df = df[(df['DOMANIALITE'] == domanialite_value) &
                     (df['STADE DE DEVELOPPEMENT'] == stade_development_value)]
    
    # Create a histogram for tree height distribution
    height_histogram = px.histogram(
        filtered_df, x='HAUTEUR (m)', title='Height Distribution'
    )
    
    # Create a histogram for tree circumference distribution
    circumference_histogram = px.histogram(
        filtered_df, x='CIRCONFERENCE (cm)', title='Circumference Distribution'
    )
    
    # Generate a scatter mapbox plot for the filtered dataset
    paris_map = px.scatter_mapbox(
        filtered_df,
        lat='lat', lon='lon',
        color='HAUTEUR (m)',   # for color scale
        size='CIRCONFERENCE (cm)',  # for size scale
        hover_name='DOMANIALITE',  # Display 'DOMANIALITE' when hover over points
        hover_data=['STADE DE DEVELOPPEMENT'],  # Additional hover info
        size_max=15,  # Maximum plot size
        opacity=0.8,  # Point opacity
        center={'lat': 48.8566, 'lon': 2.3522},  # Center Paris
        zoom=11,  # Map zoom level
        height=600  # Map height in pixels
    )
    # Set the map style
    paris_map.update_layout(mapbox_style='open-street-map')
    # Remove graph margins
    paris_map.update_layout(margin={'r': 0, 't': 0, 'l': 0, 'b': 0})

    return height_histogram, circumference_histogram, paris_map

# Run the Dash application
if __name__ == '__main__':
    app.run_server(debug=True)
