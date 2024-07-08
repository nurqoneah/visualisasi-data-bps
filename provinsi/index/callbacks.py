import dash
import pandas as pd
from dash.dependencies import Input, Output, State
from provinsi.index import plotly_visual,data_processing
from dashboard import constants
import stadata
import numpy as np


client = stadata.Client(constants.TOKEN)

def add_index_callbacks(app: dash.Dash): 
    @app.callback(
        Output('index_pie_chart_fig', 'figure'),
        [Input('index_value_type_options', 'value')],
        [Input('sub_categories_menu', 'value'),
        Input('year_dropdown', 'value'),
        Input('chart_type_options', 'value')]  
    )
    def update_pie_chart(value_type, selected_value, year, chart_type): 
        df = pd.read_csv(constants.CSV_FILE_DIRECTORY, encoding='ISO-8859-1').replace({'': np.nan})
        if selected_value in df['title'].values:
            var_id = df[df['title'] == selected_value]['var_id'].values[0]
            df_data = client.view_dynamictable(domain='1400', var=var_id)
            df_data.iloc[:, 4:] = df_data.iloc[:, 4:].replace({'': np.nan, 0: np.nan})

        pie_chart_data, _, _ = data_processing.get_pie_chart_data(df_data, year, value_type)
        if chart_type == 'pie_chart':
            fig = plotly_visual.get_pie_chart_figure(pie_chart_data, year, value_type)
        else:  
            if value_type == 'variable':
                sunburst_fig = plotly_visual.get_sunburst_chart_figure(data_processing.get_filter_df(df_data), year, path=['variable', 'turunan variable'])
            else:
                sunburst_fig = plotly_visual.get_sunburst_chart_figure(data_processing.get_filter_df(df_data), year, path=['turunan variable', 'variable'])
            fig = sunburst_fig

        fig.update_layout(
            margin=dict(l=0, r=0, t=30, b=0)
        )

        return fig

    
    @app.callback(
        Output('index_heatmap_fig', 'figure'),
        [Input('index_turunan_variabel_dropdown_heatmap', 'value'),
         Input('sub_categories_menu', 'value')],
         Input('year_dropdown', 'value')
    )
    def update_heatmap(selected_turunan_variabel, selected_sub_category, year):

        
        df = pd.read_csv(constants.CSV_FILE_DIRECTORY, encoding='ISO-8859-1').replace({'': np.nan})
        if selected_sub_category in df['title'].values:
            var_id = df[df['title'] == selected_sub_category]['var_id'].values[0]
            df_data = client.view_dynamictable(domain='1400', var=var_id)
            df_data.iloc[:, 4:] = df_data.iloc[:, 4:].replace({'': np.nan, 0: np.nan})
           
    
        df_filtered = data_processing.get_heatmap_data(df_data, year, selected_turunan_variabel)
        heatmap_fig = plotly_visual.get_heatmap_geos_figure(df_filtered, year)
        heatmap_fig.update_layout(
            margin=dict(l=0, r=0, t=30, b=0)
        )
        
        return heatmap_fig
    
        
    @app.callback(
        Output('index_bar_chart_fig', 'figure'),
        [Input('index_value_type_options_bar', 'value')],
        [Input('sub_categories_menu', 'value'),
        Input('year_dropdown', 'value'),
        Input('index_chart_type_options_bar', 'value')]  
    )
    def update_bar_chart(value_type, selected_value, year, chart_type): 
        df = pd.read_csv(constants.CSV_FILE_DIRECTORY, encoding='ISO-8859-1').replace({'': np.nan})
        if selected_value in df['title'].values:
            var_id = df[df['title'] == selected_value]['var_id'].values[0]
            df_data = client.view_dynamictable(domain='1400', var=var_id)
            df_data.iloc[:, 4:] = df_data.iloc[:, 4:].replace({'': np.nan, 0: np.nan})

        bar_chart_data, _, _ = data_processing.get_bar_chart_data(df_data, year, value_type)
        if chart_type == 'bar_chart':
            fig = plotly_visual.get_bar_chart_figure(bar_chart_data, year, value_type)
        else: 
            if value_type == 'variable':
                stacked_bar_fig = plotly_visual.get_stacked_bar_chart_figure(data_processing.get_filter_df(df_data), year, path=['variable', 'turunan variable'])
            else:
                stacked_bar_fig = plotly_visual.get_stacked_bar_chart_figure(data_processing.get_filter_df(df_data), year, path=['turunan variable', 'variable'])
            fig = stacked_bar_fig

        fig.update_layout(
            margin=dict(l=0, r=0, t=30, b=0)
        )

        return fig
        
        
    @app.callback(
        Output('index_time_series_fig', 'figure'),
        [Input('index_turunan_variabel_dropdown_time_series', 'value'),
        Input('index_variables_multi_select', 'value'),  
        Input('sub_categories_menu', 'value')]
    )
    def update_time_series(turunan_variable, selected_variables, selected_value):
       
        df = pd.read_csv(constants.CSV_FILE_DIRECTORY, encoding='ISO-8859-1')
        if selected_value in df['title'].values:
            var_id = df[df['title'] == selected_value]['var_id'].values[0]
            df_data = client.view_dynamictable(domain='1400', var=var_id)
            df_data.iloc[:, 4:] = df_data.iloc[:, 4:].replace({'': np.nan, 0: np.nan})
          
            filtered_df = df_data[(df_data['turunan variable'] == turunan_variable) & (df_data['variable'].isin(selected_variables))]

            time_series_data = data_processing.get_time_series_data(df_data, turunan_variable, selected_variables)
            
            time_series_fig = plotly_visual.get_time_series_figure(time_series_data)
            
            return time_series_fig

   
    
            

        
                
