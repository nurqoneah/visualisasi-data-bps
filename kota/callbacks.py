import pandas as pd
import numpy as np
from dash import html
from dash.dcc import send_data_frame
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from dashboard import constants
from kota import data_processing, plotly_visual
from kota.dlayout import city_analysis_dlayout
import stadata


client = stadata.Client(constants.TOKEN)


def add_city_callbacks(app):
    df = pd.read_csv(constants.CSV_FILE_DIRECTORY_CITY, encoding='ISO-8859-1')
    df = df.replace({'': np.nan})
    city = constants.DATA_KOTA_DF

    @app.callback(
        Output('categories_menu_kota', 'data'),
        Output('categories_menu_kota', 'value'),
        [Input('cities_menu', 'value')]
    )
    def update_categories_kota(selected_city):
        if not selected_city:
            raise PreventUpdate

        selected_city_id = int(city[city['variable_kota'] == selected_city]['id_var_kota'].values[0])
        categories = df[df['domain'] == selected_city_id]['sub_name'].unique().tolist()
        categories = ['Semua Kategori'] + categories

        return [{'label': category, 'value': category} for category in categories], categories[0] if categories else None

    @app.callback(
        Output('sub_categories_menu_kota', 'data'),
        Output('sub_categories_menu_kota', 'value'),
        [Input('categories_menu_kota', 'value'), Input('cities_menu', 'value')]
    )
    def update_sub_categories_kota(selected_category, selected_city):
        if not selected_category or not selected_city:
            raise PreventUpdate

        selected_city_id = int(city[city['variable_kota'] == selected_city]['id_var_kota'].values[0])
        if selected_category == 'Semua Kategori':
            sub_categories = df[df['domain'] == selected_city_id]['title'].unique().tolist()
        else:
            sub_categories = df[(df['domain'] == selected_city_id) & (df['sub_name'] == selected_category)]['title'].unique().tolist()
        return [{'label': sub_category, 'value': sub_category} for sub_category in sub_categories], sub_categories[0] if sub_categories else None

    @app.callback(
        Output('year_dropdown_kota', 'value'),
        Output('year_dropdown_kota', 'data'),
        [Input('sub_categories_menu_kota', 'value'), Input('cities_menu', 'value')]
    )
    def update_year_kota(selected_sub_category, selected_city):
        if not selected_sub_category or not selected_city:
            raise PreventUpdate

        selected_city_id = int(city[city['variable_kota'] == selected_city]['id_var_kota'].values[0])
        if selected_sub_category in df['title'].values:
            var_id = df[(df['domain'] == selected_city_id) & (df['title'] == selected_sub_category)]['var_id'].values[0]
            try:
                df_data = client.view_dynamictable(domain=selected_city_id, var=var_id)
                df_data.iloc[:, 4:] = df_data.iloc[:, 4:].replace({'': np.nan, 0: np.nan})
                years = df_data.columns[4:].tolist()
                current_year = str(pd.Timestamp.now().year)
                default_year = current_year if current_year in years else years[-1] if years else None
                years_options = [{'label': year, 'value': year} for year in years]
                return default_year, years_options
            except Exception as e:
                print(f"Error fetching data: {e}")
                return None, []
        else:
            return None, []
        
    @app.callback(
        Output('download_excel_kota', 'data'),
        [Input('download_excel_button_kota', 'n_clicks')],
        [State('sub_categories_menu_kota', 'value'), State('year_dropdown_kota', 'value'), State('cities_menu', 'value')]
    )
    def update_download_link_kota(n_clicks, selected_sub_category, year, selected_city):
        if not n_clicks:
            raise PreventUpdate

        if selected_sub_category is None or year is None or selected_city is None:
            raise PreventUpdate

        selected_city_id = int(city[city['variable_kota'] == selected_city]['id_var_kota'].values[0])
        if selected_sub_category in df['title'].values:
            var_id = df[(df['domain'] == selected_city_id) & (df['title'] == selected_sub_category)]['var_id'].values[0]
            try:
                df_data = client.view_dynamictable(domain=selected_city_id, var=var_id)
                df_data.iloc[:, 4:] = df_data.iloc[:, 4:].replace({'': np.nan, 0: np.nan})
                excel_data = pd.DataFrame(df_data)
                return send_data_frame(excel_data.to_excel, "Data.xlsx")
            except Exception as e:
                print(f"Error fetching data: {e}")
                raise PreventUpdate
        else:
            raise PreventUpdate

  
        
    @app.callback(
        Output('dynamic-content-kota', 'children'),
        [Input('sub_categories_menu_kota', 'value'),
        Input('year_dropdown_kota', 'value'),
        Input('cities_menu', 'value')]
    )
    def update_layout_kota(selected_value, year, selected_city):
        if selected_value in df['title'].values:
            selected_city_id = int(city[city['variable_kota'] == selected_city]['id_var_kota'].values[0])
            var_id = df[df['title'] == selected_value]['var_id'].values[0]
            vertical_id = df[df['title'] == selected_value]['vertical'].values[0]
            turunan_id = df[df['title'] == selected_value]['turunan_variabel_id'].values[0]
            unit = df[df['title'] == selected_value]['unit'].values[0]

            df_data = client.view_dynamictable(domain=selected_city_id, var=var_id)
            df_data.iloc[:, 4:] = df_data.iloc[:, 4:].replace({'': np.nan})

            if year not in df_data.columns:
                return html.Div(f"Year {year} not found in the data")

            return city_analysis_dlayout(unit, selected_value, df_data, year, vertical_id, turunan_id)
       
        else:
            return html.Div("Selected value not found in the dataset")


    @app.callback(
        Output('city_time_series_fig_kota', 'figure'),
        [Input('city_turunan_variabel_dropdown_time_series_kota', 'value'),
        Input('city_variables_multi_select_kota', 'value'),  
        Input('sub_categories_menu_kota', 'value'),
        Input('cities_menu', 'value')]
    )
    def update_time_series(turunan_variable, selected_variables, selected_value, selected_city):
       
        if selected_value in df['title'].values:
            selected_city_id = int(city[city['variable_kota'] == selected_city]['id_var_kota'].values[0])
            var_id = df[df['title'] == selected_value]['var_id'].values[0]
            df_data = client.view_dynamictable(domain=selected_city_id, var=var_id)
            df_data.iloc[:, 4:] = df_data.iloc[:, 4:].replace({'': np.nan, 0: np.nan})

            filtered_df = df_data[(df_data['turunan variable'] == turunan_variable) & (df_data['variable'].isin(selected_variables))]

            time_series_data = data_processing.get_time_series_data(filtered_df, turunan_variable, selected_variables)

            time_series_fig = plotly_visual.get_time_series_figure(time_series_data)

            return time_series_fig


        