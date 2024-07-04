import dash
import pandas as pd
from dash.dependencies import Input, Output, State
from provinsi.other import plotly_visual,data_processing
from dashboard import constants
import stadata
import numpy as np


client = stadata.Client(constants.TOKEN)

def add_other_callbacks(app: dash.Dash): 
    
    @app.callback(
        Output('other_time_series_fig', 'figure'),
        [Input('other_turunan_variabel_dropdown_time_series', 'value'),
        Input('other_variables_multi_select', 'value'),  
        Input('sub_categories_menu', 'value')]
    )
    def update_time_series(turunan_variable, selected_variables, selected_value):
        # Baca data dari otherber data Anda
        df = pd.read_csv(constants.CSV_FILE_DIRECTORY, encoding='ISO-8859-1')
        if selected_value in df['title'].values:
            var_id = df[df['title'] == selected_value]['var_id'].values[0]
            df_data = client.view_dynamictable(domain='1400', var=var_id)
            df_data.iloc[:, 4:] = df_data.iloc[:, 4:].replace({'': np.nan, 0: np.nan})
            df_data = data_processing.preprocess_dataframe(df_data)
            filtered_df = df_data[(df_data['turunan variable'] == turunan_variable) & (df_data['variable'].isin(selected_variables))]

            time_series_data = data_processing.get_time_series_data(filtered_df, turunan_variable, selected_variables)
            
            time_series_fig = plotly_visual.get_time_series_figure(time_series_data)
            
            return time_series_fig
    @app.callback(
        Output('other_heatmap_fig', 'figure'),
        [Input('other_turunan_variabel_dropdown_heatmap', 'value'),
         Input('sub_categories_menu', 'value')],
         Input('year_dropdown', 'value')
    )
    def update_heatmap(selected_turunan_variabel, selected_sub_category, year):

        
        df = pd.read_csv(constants.CSV_FILE_DIRECTORY, encoding='ISO-8859-1').replace({'': np.nan})
        if selected_sub_category in df['title'].values:
            var_id = df[df['title'] == selected_sub_category]['var_id'].values[0]
            df_data = client.view_dynamictable(domain='1400', var=var_id)
            df_data.iloc[:, 4:] = df_data.iloc[:, 4:].replace({'': np.nan, 0: np.nan})
            print("holaa")
            print(df_data)
    
        df_filtered = data_processing.get_heatmap_data(df_data, year, selected_turunan_variabel)
        heatmap_fig = plotly_visual.get_heatmap_geos_figure(df_filtered, year)
        heatmap_fig.update_layout(
            margin=dict(l=0, r=0, t=30, b=0)
        )
        
        return heatmap_fig
    
    
            

        
                
