import pandas as pd
import numpy as np
from dash import html
from dash.dcc import send_data_frame
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from dashboard import constants
import stadata
from provinsi.sum.layout import sum_analysis_layout
from provinsi.average.layout import average_analysis_layout
from provinsi.percent.layout import percent_analysis_layout
from provinsi.index.layout import index_analysis_layout
from provinsi.climate.layout import climate_analysis_layout
from provinsi.other.layout import other_analysis_layout

client = stadata.Client(constants.TOKEN)

def add_province_callbacks(app):
    df = pd.read_csv(constants.CSV_FILE_DIRECTORY, encoding='ISO-8859-1')
    df = df.replace({'': np.nan})

    @app.callback(
        Output('sub_categories_menu', 'data'),
        Output('sub_categories_menu', 'value'),
        [Input('categories_menu', 'value')]
    )
    def update_sub_categories(selected_category):
        if selected_category == 'Semua Kategori':
            sub_categories = df['title'].unique().tolist()
        else:
            sub_categories = df[df['sub_name'] == selected_category]['title'].unique().tolist()
        return [{'label': sub_category, 'value': sub_category} for sub_category in sub_categories], sub_categories[0] if sub_categories else None

    @app.callback(
        Output('dynamic-content', 'children'),
        [Input('sub_categories_menu', 'value'),
         Input('year_dropdown', 'value')]
    )
    def update_layout(selected_value, year):
        if selected_value in df['title'].values:
            var_id = df[df['title'] == selected_value]['var_id'].values[0]
            jenis_data = df[df['title'] == selected_value]['jenis_data'].values[0]
            vertical_id = df[df['title'] == selected_value]['vertical'].values[0]
            turunan_id = df[df['title'] == selected_value]['turunan_variabel_komposisi_id'].values[0]
            sub_id = df[df['title'] == selected_value]['sub_id'].values[0]
            unit = df[df['title'] == selected_value]['unit'].values[0]

            df_data = client.view_dynamictable(domain='1400', var=var_id)
            df_data.iloc[:, 4:] = df_data.iloc[:, 4:].replace({'': np.nan})

            if year not in df_data.columns:
                return html.Div(f"Year {year} not found in the data")

            if jenis_data == 1:
                return sum_analysis_layout(unit, selected_value, df_data, year, vertical_id, turunan_id)
            elif jenis_data == 2:
                return average_analysis_layout(unit, selected_value, df_data, year, vertical_id, turunan_id)
            elif jenis_data == 3:
                return percent_analysis_layout(unit, selected_value, df_data, year, vertical_id, turunan_id)
            elif jenis_data == 4:
                return index_analysis_layout(unit, selected_value, df_data, year, vertical_id, turunan_id)
            elif jenis_data == 5:
                return climate_analysis_layout(unit, selected_value, df_data, year, turunan_id)
            elif jenis_data == 6:
                return other_analysis_layout(unit, selected_value,df_data, year, vertical_id, turunan_id, sub_id)
            else:
                return html.Div("No layout available for the selected category")
        else:
            return html.Div("Selected value not found in the dataset")

    @app.callback(
        Output('year_dropdown', 'value'),
        Output('year_dropdown', 'data'),
        [Input('sub_categories_menu', 'value')]
    )
    def update_year(selected_sub_category):
        if selected_sub_category in df['title'].values:
            var_id = df[df['title'] == selected_sub_category]['var_id'].values[0]
            df_data = client.view_dynamictable(domain='1400', var=var_id)
            df_data.iloc[:, 4:] = df_data.iloc[:, 4:].replace({'': np.nan, 0: np.nan})
            years = df_data.columns[4:].tolist()
            current_year = str(pd.Timestamp.now().year)
            default_year = current_year if current_year in years else years[-1] if years else None
            years_options = [{'label': year, 'value': year} for year in years]
            return default_year, years_options
        else:
            return None, []

   
    @app.callback(
        Output('download_excel', 'data'),
        [Input('download_excel_button', 'n_clicks')],
        [State('sub_categories_menu', 'value'), State('year_dropdown', 'value')]
    )
    def update_download_link(n_clicks, selected_sub_category, year):
        if not n_clicks:
            raise PreventUpdate

        if selected_sub_category is None or year is None:
            raise PreventUpdate

        if selected_sub_category in df['title'].values:
            var_id = df[df['title'] == selected_sub_category]['var_id'].values[0]
            df_data = client.view_dynamictable(domain='1400', var=var_id)
            df_data.iloc[:, 4:] = df_data.iloc[:, 4:].replace({'': np.nan, 0: np.nan})

            
            
            excel_data = pd.DataFrame(df_data)
            return send_data_frame(excel_data.to_excel, "Data.xlsx")

        else:
            raise PreventUpdate  
        
    callback_ids=["total","max","min","growth","top_growth","average"]
    for callback_id in callback_ids:
        @app.callback(
            Output(f'{callback_id}-info-modal', 'opened'),
            Input(f'{callback_id}-question-icon', 'n_clicks'),
            prevent_initial_call=True
        )
        def toggle_modal(n_clicks):
            if n_clicks:
                return True
            return False   

       