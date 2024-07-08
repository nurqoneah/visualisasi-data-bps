import numpy as np
import pandas as pd

def get_filter_df(df):
    df = df[~df['variable'].str.contains('Riau|Provinsi Riau|Jumlah|Jumlah bukan makanan|Jumlah Makanan|PDRB', case=False) & ~df['turunan variable'].str.contains('Jumlah', case=False)]
    return df
def get_total(df,year):
  if year not in df.columns:
        return None
  filtered_df = get_filter_df(df)
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
            total_changen = "{:,.2f} ".format(total_change)+unit
            if total_change > 0:
                total_change_str = "+" + total_changen
            else:
                total_change_str = total_changen
            return 'Total '+title, "{:,.2f} ".format(total_current_year) +unit, total_change_str +unit
        else:
        
            return 'Total '+title, "{:,.2f} ".format(total_current_year)+unit, None
    else:
        return 'Total '+title, None, None

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


def get_pie_chart_data(df, year, chart_type):
   
    df_filtered = df[~df['variable'].str.contains('Riau|Provinsi Riau|Jumlah|Jumlah bukan makanan|Jumlah Makanan|PDRB', case=False)]
    
    if 'Jumlah' in df_filtered['turunan variable'].unique():
        df_filtered = df_filtered[df_filtered['turunan variable'] != 'Jumlah'] 

    if chart_type == 'variable':
        pie_data = df_filtered[['variable', year]].groupby('variable').sum().reset_index()
    else:  
        pie_data = df_filtered[['turunan variable', year]].groupby('turunan variable').sum().reset_index()
    
    unique_turunan_var = df_filtered['turunan variable'].unique()
    return pie_data, unique_turunan_var, chart_type


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

def get_bar_chart_data(df, year, chart_type):
    
    df_filtered = df[~df['variable'].str.contains('Riau|Provinsi Riau|Jumlah|Jumlah bukan makanan|Jumlah Makanan|PDRB', case=False)]
    
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


def preprocess_dataframe(df):
    if 'Jumlah' not in df['turunan variable'].unique():
        numeric_columns = df.columns[4:]
        sum_df = df.groupby(['id_var', 'variable'])[numeric_columns].sum().reset_index()
        sum_df['id_tur_var'] = 'Jumlah'
        sum_df['turunan variable'] = 'Jumlah'

       
        df = pd.concat([df, sum_df], ignore_index=True)
        
        
    return df

def get_time_series_data(df, turunan_variable, year):
  
    filtered_df = df[(df['turunan variable'] == turunan_variable)]
    
  
    variables = filtered_df['variable'].tolist()
    values = filtered_df[year].tolist()

   
    trace = {
        'x': variables,
        'y': values,
        'mode': 'lines+markers',
        'name': f'{turunan_variable} {year}'
    }

    return [trace]
