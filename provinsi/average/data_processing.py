import numpy as np
import pandas as pd

def get_average(df, year):
    print(df)
    if year not in df.columns:
        return None
    riau_df = df[df['variable'].str.contains('Riau|Provinsi Riau|Jumlah', case=False)]
    print(riau_df)
    if not riau_df.empty:
        riau_value = riau_df[year].sum()
        return riau_value
    else:
        return None
def get_filter_df(df):
    df = df[~df['variable'].str.contains('Riau|Provinsi Riau|Jumlah|Jumlah bukan makanan|Jumlah Makanan|PDRB', case=False) & ~df['turunan variable'].str.contains('Jumlah', case=False)]
    return df

def get_average_change(unit, df, year, title):
    average_current_year = get_average(df, year)
    average_previous_year = get_average(df, str(int(year) - 1))
    
    if average_current_year is not None:
        if average_previous_year is not None:
            average_change = average_current_year - average_previous_year
            average_changen = "{:,.2f} ".format(average_change)+unit
            if average_change > 0:
                average_change_str = "+" + average_changen
            else:
                average_change_str = average_changen
            return 'Rata-rata '+title,  "{:,.2f} ".format(average_current_year)+unit, average_change_str
        else:
            # Handle case when previous year data is missing
            return 'Rata-rata '+title,  "{:,.2f} ".format(average_current_year)+unit, None
    else:
        return 'Rata-rata '+title, None, None

def get_min(unit, df, year, title):
    filtered_df = get_filter_df(df)
    if not filtered_df.empty:
        min_row = filtered_df.groupby('variable')[year].sum().reset_index().sort_values(year, ascending=True).iloc[0]
    else:
        min_row = df.groupby('variable')[year].sum().reset_index().sort_values(year, ascending=True).iloc[0]
    return 'Min '+title, "{:,.2f} ".format(min_row[year])+unit, min_row['variable']

def get_max(unit, df, year, title):
    filtered_df = get_filter_df(df)
    if not filtered_df.empty:
        max_row = filtered_df.groupby('variable')[year].sum().reset_index().sort_values(year, ascending=False).iloc[0]
    else:
        max_row = df.groupby('variable')[year].sum().reset_index().sort_values(year, ascending=False).iloc[0]
    return 'Max '+title, "{:,.2f} ".format(max_row[year])+unit, max_row['variable']

def get_growth(df, year, title):
    previous_year = str(int(year) - 1)
    average_latest = get_average(df, year)
    average_previous = get_average(df, previous_year)
  
    if average_latest is not None:
        if average_previous is not None:
            if average_previous != 0:
                growth = ((average_latest - average_previous) / average_previous) * 100
            else:
                growth = float('inf')
            return 'Growth',"{:,.2f}%".format(growth)
        else:
            # Handle case when previous year data is missing
            return 'Growth', None
    else:
        return 'Growth '+title, None

def get_top_growth(df, year, title):
    
    filtered_df = df[~df['variable'].str.contains('Riau|Provinsi Riau|Jumlah|Jumlah bukan makanan|Jumlah Makanan|PDRB', case=False) & ~df['turunan variable'].str.contains('Jumlah', case=False)]
    previous_year = str(int(year) - 1)

    if year not in df.columns or previous_year not in df.columns:
        return 'Top Growth', None, None

    if not filtered_df.empty:
        sum_df = filtered_df.groupby('variable')[[year, previous_year]].sum()
        sum_df['growth'] = ((sum_df[year] - sum_df[previous_year]) / sum_df[previous_year]) * 100

        if not sum_df.empty:
            top_growth_row = sum_df[sum_df['growth'] == sum_df['growth'].max()]
            top_growth = top_growth_row['growth'].iloc[0]
            top_variable = top_growth_row.index[0]
            return 'Top Growth', "{:,.2f}%".format(top_growth), top_variable 

    return 'Top Growth '+title, None, None

def get_scatter_plot_data(df, year):
    df_filtered = df[~df['variable'].str.contains('Riau|Provinsi Riau|Jumlah|Jumlah bukan makanan|Jumlah Makanan|PDRB', case=False)]
    return df_filtered[['variable', 'turunan variable', year]]

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

    # Select relevant columns
    df_filtered = df_filtered[['id_var', 'variable', 'id_tur_var', 'turunan variable', year]]

    return df_filtered

def get_bar_chart_data(df, year, chart_type):
    # Filter out rows containing certain keywords in 'variable'
    df_filtered = df[~df['variable'].str.contains('Riau|Provinsi Riau|Jumlah|Jumlah bukan makanan|Jumlah Makanan|PDRB', case=False)]
    
    if chart_type == 'variable':
        if 'Jumlah' in df_filtered['turunan variable'].unique():
            df_filtered = df_filtered[df_filtered['turunan variable'] != 'Jumlah']  # Remove categories with 'Jumlah'
        bar_data = df_filtered[['variable', year]].groupby('variable').sum().reset_index()
    else:  # chart_type == 'variable_turunan'
        if 'Jumlah' in df_filtered['turunan variable'].unique():
            df_filtered = df_filtered[df_filtered['turunan variable'] != 'Jumlah']  # Remove categories with 'Jumlah'
        bar_data = df_filtered[['turunan variable', year]].groupby('turunan variable').sum().reset_index()
    
    unique_turunan_var = df_filtered['turunan variable'].unique()
    return bar_data, unique_turunan_var, chart_type

def get_time_series_data(df, turunan_variable, selected_variables):
    filtered_df = df[(df['turunan variable'] == turunan_variable) & (df['variable'].isin(selected_variables))]

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

