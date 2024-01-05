# Prepare environment
from dash import dcc, html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import numpy as np
import plotly.express as px
import pandas as pd

# Load csv
data = pd.read_csv("arbres10percent.csv")

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
    
    