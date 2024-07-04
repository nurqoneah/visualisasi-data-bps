import dash
import pandas as pd
from dash.dependencies import Input, Output, State
from provinsi.percent import plotly_visual,data_processing
from dashboard import constants
import stadata
import numpy as np


client = stadata.Client(constants.TOKEN)

def add_percent_callbacks(app: dash.Dash): 
    @app.callback(
        Output('percent_pie_chart_fig', 'figure'),
        [Input('sub_categories_menu', 'value'),
        Input('year_dropdown', 'value'),
        Input('percent_chart_type_options', 'value')]  
    )
    def update_pie_chart(selected_value, year, chart_type):  
        df = pd.read_csv(constants.CSV_FILE_DIRECTORY, encoding='ISO-8859-1').replace({'': np.nan})
        if selected_value in df['title'].values:
            var_id = df[df['title'] == selected_value]['var_id'].values[0]
            df_data = client.view_dynamictable(domain='1400', var=var_id)
            df_data.iloc[:, 4:] = df_data.iloc[:, 4:].replace({'': np.nan, 0: np.nan})

        pie_chart_data = data_processing.get_filter_df(df_data)
        if chart_type == 'pie_chart':
            fig = plotly_visual.get_mul_pie_chart_figure(pie_chart_data, year)
        else:  
            
            sunburst_fig = plotly_visual.get_sunburst_chart_figure(data_processing.get_filter_df(df_data), year)
            fig = sunburst_fig

        fig.update_layout(
            margin=dict(l=0, r=0, t=30, b=0)
        )

        return fig

    

        
   
        


    
            

        
                
