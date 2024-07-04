import numpy as np
import pandas as pd

def get_filter_df(df):
    df = df[~df['variable'].str.contains('Riau|Provinsi Riau|Jumlah|Jumlah bukan makanan|Jumlah Makanan|PDRB', case=False) & ~df['turunan variable'].str.contains('Jumlah', case=False)]
    return df


def get_min(unit, df, year, title):
    df = df[~df['variable'].str.contains('Riau|Provinsi Riau|Jumlah|Jumlah bukan makanan|Jumlah Makanan|PDRB', case=False)]
    if 'Jumlah' in df['turunan variable'].unique():
        min_row = df[df['turunan variable'] == 'Jumlah'].groupby('variable')[year].sum().reset_index().sort_values(year, ascending=True).iloc[0]
    else:
        min_row = df.groupby('variable')[year].sum().reset_index().sort_values(year, ascending=True).iloc[0]
    return 'Min '+title, "{:,.2f} ".format(min_row[year])+unit, min_row['variable']

def get_max(unit, df, year, title):
    df = df[~df['variable'].str.contains('Riau|Provinsi Riau|Jumlah|Jumlah bukan makanan|Jumlah Makanan|PDRB', case=False)]
    if 'Jumlah' in df['turunan variable'].unique():
        max_row = df[df['turunan variable'] == 'Jumlah'].groupby('variable')[year].sum().reset_index().sort_values(year, ascending=False).iloc[0]
    else:
        max_row = df.groupby('variable')[year].sum().reset_index().sort_values(year, ascending=False).iloc[0]
    return 'Max '+title, "{:,.2f} ".format(max_row[year])+unit, max_row['variable']





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



def preprocess_dataframe(df):
    if 'Jumlah' not in df['turunan variable'].unique():
        numeric_columns = df.columns[4:]
        sum_df = df.groupby(['id_var', 'variable'])[numeric_columns].sum().reset_index()
        sum_df['id_tur_var'] = 'Jumlah'
        sum_df['turunan variable'] = 'Jumlah'

        # Concatenate the original dataframe with the sum dataframe
        df = pd.concat([df, sum_df], ignore_index=True)
        
        
    return df

def get_time_series_data(df):
    filtered_df = df

    years = df.columns[4:].tolist()
    traces = []

    # Iterate through selected variables
    for variable in selected_variables:
        variable_data = filtered_df[filtered_df['variable'] == variable]
        if variable_data.empty:
            print(f"No data found for variable '{variable}' within the filtered dataframe.")
            continue
        
        try:
            data = variable_data.iloc[0, 4:].tolist()
            trace = {
                'x': years,
                'y': data,
                'mode': 'lines+markers',
                'name': variable
            }

            # Append the trace to the list of traces
            traces.append(trace)
        except IndexError as e:
            print(f"IndexError for variable '{variable}': {e}")
            continue
    return traces

