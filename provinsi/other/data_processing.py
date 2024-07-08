import numpy as np
import pandas as pd
import dash_mantine_components as dmc

def get_filter_df(df):
    df = df[~df['variable'].str.contains('Riau|Provinsi Riau|Jumlah|Jumlah bukan makanan|Jumlah Makanan|PDRB', case=False) & ~df['turunan variable'].str.contains('Jumlah', case=False)]
    return df


def get_min(unit, df, year, title):
    df = df[~df['variable'].str.contains('Riau|Provinsi Riau|Jumlah|Jumlah bukan makanan|Jumlah Makanan|PDRB|Neraca Perdagangan Luar Negeri', case=False)]
    if 'Jumlah' in df['turunan variable'].unique():
        grouped_df = df[df['turunan variable'] == 'Jumlah'].groupby('variable')[year].sum().reset_index().sort_values(year, ascending=True)
    else:
        grouped_df = df.groupby('variable')[year].sum().reset_index().sort_values(year, ascending=True)
    if grouped_df.empty:
        return 'Min ' + title, None, None
    
    min_row = grouped_df.iloc[0]
    return 'Min ' + title, "{:,.2f} ".format(min_row[year]) + unit, min_row['variable']

def get_max(unit, df, year, title):
    df = df[~df['variable'].str.contains('Riau|Provinsi Riau|Jumlah|Jumlah bukan makanan|Jumlah Makanan|PDRB', case=False)]
    if 'Jumlah' in df['turunan variable'].unique():
        grouped_df = df[df['turunan variable'] == 'Jumlah'].groupby('variable')[year].sum().reset_index().sort_values(year, ascending=False)
    else:
        grouped_df = df.groupby('variable')[year].sum().reset_index().sort_values(year, ascending=False)
    if grouped_df.empty:
        return 'Max ' + title, None, None
    
    max_row = grouped_df.iloc[0]
    return 'Max ' + title, "{:,.2f} ".format(max_row[year]) + unit, max_row['variable']


def get_heatmap_data(df, year, selected_turunan_variabel):
    df_filtered = df[~df['variable'].str.contains('Riau|Provinsi Riau', case=False)]
    if selected_turunan_variabel is not None:
        if 'Jumlah' not in df_filtered['turunan variable'].unique():
            df_sum = df_filtered.groupby(['id_var', 'variable'], as_index=False)[year].sum()
            df_sum['id_tur_var'] = 'Jumlah'
            df_sum['turunan variable'] = 'Jumlah'
            df_filtered = pd.concat([df_filtered, df_sum], ignore_index=True)
    
        if selected_turunan_variabel not in ['Jumlah']:
            df_filtered = df_filtered[df_filtered['turunan variable'] == selected_turunan_variabel]
        else:
            df_filtered = df_filtered[df_filtered['turunan variable'] == 'Jumlah']

    
    df_filtered = df_filtered[['id_var', 'variable', 'id_tur_var', 'turunan variable', year]]

    return df_filtered


def get_time_series_data(df, turunan_variable, selected_variables):
    filtered_df = df[(df['turunan variable'] == turunan_variable) & (df['variable'].isin(selected_variables))]

    years = df.columns[4:].tolist()
    traces = []

   
    for variable in selected_variables:
        variable_data = filtered_df[filtered_df['variable'] == variable]
        if variable_data.empty:
            return dmc.Alert(f"No data found for variable '{variable}' within the filtered dataframe.", color="red", title="Connection Error")

            continue
        
        try:
            data = variable_data.iloc[0, 4:].tolist()
            trace = {
                'x': years,
                'y': data,
                'mode': 'lines+markers',
                'name': variable
            }

         
            traces.append(trace)
        except IndexError as e:
            return dmc.Alert(f"IndexError for variable '{variable}': {e}", color="red", title="Connection Error")

    return traces

