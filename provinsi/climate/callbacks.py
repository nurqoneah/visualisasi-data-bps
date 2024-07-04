import dash
import pandas as pd
from dash.dependencies import Input, Output, State
from provinsi.climate import plotly_visual,data_processing
from dashboard import constants
import stadata
import numpy as np


client = stadata.Client(constants.TOKEN)

def add_climate_callbacks(app: dash.Dash): 
    
    @app.callback(
        Output('climate_time_series_fig', 'figure'),
        [Input('climate_turunan_variabel_dropdown_time_series', 'value'),
         Input('sub_categories_menu', 'value')],
         Input('year_dropdown', 'value')
    )
    def update_time_series(selected_turunan_variabel, selected_sub_category, year):

        
        df = pd.read_csv(constants.CSV_FILE_DIRECTORY, encoding='ISO-8859-1').replace({'': np.nan})
        if selected_sub_category in df['title'].values:
            var_id = df[df['title'] == selected_sub_category]['var_id'].values[0]
            df_data = client.view_dynamictable(domain='1400', var=var_id)
            df_data.iloc[:, 4:] = df_data.iloc[:, 4:].replace({'': np.nan, 0: np.nan})
    
        df_filtered = data_processing.get_time_series_data(df_data,selected_turunan_variabel, year)
        time_series_figure = plotly_visual.get_time_series_figure(df_filtered)
        time_series_figure.update_layout(
            margin=dict(l=0, r=0, t=30, b=0)
        )
        
        return time_series_figure
    
    
            

        
                
