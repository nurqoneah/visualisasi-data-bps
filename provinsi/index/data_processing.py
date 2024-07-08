import numpy as np
import pandas as pd
import dash_mantine_components as dmc


def get_total(df,year):
    if year not in df.columns:
            return None
 
    filtered_df = df[df['variable'].str.contains('Riau|Provinsi Riau|Jumlah|Jumlah bukan makanan|Jumlah Makanan|PDRB|Neraca Perdagangan Luar Negeri', case=False) ]
    
    if 'Jumlah|Total' in filtered_df['turunan variable'].unique():
        filtered_df=filtered_df[filtered_df['turunan variable'].str.contains('Jumlah|Total', case=False) ]
    if not filtered_df.empty:
        total = filtered_df[year].sum()
    else:
        total = df[year].sum()
   
    return total

def get_total_change(unit,df, year, title):
    total_current_year = get_total(df, year)
    total_previous_year = get_total(df, str(int(year) - 1))
    
    if total_current_year is not None:
        if total_previous_year is not None:
            total_change = total_current_year - total_previous_year
            total_changen = "{:,.2f} ".format(total_change)+ unit
            if total_change > 0:
                total_change_str = "+" + total_changen
            else:
                total_change_str = total_changen
            return title, "{:,.2f} ".format(total_current_year)+unit, total_change_str
        else:
            return title, "{:,.2f} ".format(total_current_year)+unit, None
    else:
        return title, None, None

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


def get_growth(df, year, title):
    previous_year = str(int(year) - 1)
    total_latest = get_total(df, year)
    total_previous = get_total(df, previous_year)
  
    if total_latest is not None:
        if total_previous is not None:
            if total_previous != 0:
                growth = ((total_latest - total_previous) / total_previous) * 100
            else:
                growth = float('inf')
            return 'Growth',"{:,.2f}%".format(growth)
        else:
            
            return 'Growth', None
    else:
        return 'Growth '+title, None


def get_heatmap_data(df, year, selected_turunan_variabel):
    df_filtered = df[~df['variable'].str.contains('Riau|Provinsi Riau', case=False)]
 
    if selected_turunan_variabel is not None:
        df_filtered = df_filtered[df_filtered['turunan variable'] == selected_turunan_variabel]
    df_filtered = df_filtered[['id_var', 'variable', 'id_tur_var', 'turunan variable', year]]

    return df_filtered

def get_bar_chart_data(df, year, chart_type):
   
    df_filtered = df
    if chart_type == 'variable':
        if 'Jumlah' in df_filtered['turunan variable'].unique():
            df_filtered = df_filtered[df_filtered['turunan variable'] != 'Jumlah'] 
        bar_data = df_filtered[['variable', year]].groupby('variable').sum().reset_index()
    else: 
        if 'Jumlah' in df_filtered['turunan variable'].unique():
            df_filtered = df_filtered[df_filtered['turunan variable'] != 'Jumlah']  
        bar_data = df_filtered[['turunan variable', year]].groupby('turunan variable').sum().reset_index()
    
    unique_turunan_var = df_filtered['turunan variable'].unique()
    return bar_data, unique_turunan_var, chart_type


def get_time_series_data(df, turunan_variable, selected_variables):
    filtered_df = df[(df['turunan variable'] == turunan_variable) & (df['variable'].isin(selected_variables))]

    years = df.columns[4:].tolist()
    traces = []

     
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

         
            traces.append(trace)
        except IndexError as e:
            return dmc.Alert(f"IndexError for variable '{variable}': {e}", color="red", title="Index Error")
    return traces

