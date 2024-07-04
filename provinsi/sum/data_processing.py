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

def get_total_change(unit, df, year, title):
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
            return 'Total '+title, "{:,.2f} ".format(total_current_year) +unit, total_change_str
        else:
            # Handle case when previous year data is missing
            return 'Total '+title, "{:,.2f} ".format(total_current_year)+unit, None
    else:
        return 'Total '+title, None, None

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
            # Handle case when previous year data is missing
            return 'Growth', None
    else:
        return 'Growth '+title, None

def get_top_growth(df, year, title):
    # Filter out rows containing certain keywords and 'Jumlah' in 'turunan variable'
    filtered_df = df[~df['variable'].str.contains('Riau|Provinsi Riau|Jumlah|Jumlah bukan makanan|Jumlah Makanan|PDRB', case=False) & ~df['turunan variable'].str.contains('Jumlah', case=False)]
    previous_year = str(int(year) - 1)

    if year not in df.columns or previous_year not in df.columns:
        return 'Top Growth', None, None

    if not filtered_df.empty:
        sum_df = filtered_df.groupby('variable')[[year, previous_year]].sum()
        sum_df[previous_year].replace(0, np.nan, inplace=True)
        sum_df['growth'] = ((sum_df[year] - sum_df[previous_year]) / sum_df[previous_year]) * 100

        if not sum_df.empty:
            top_growth_row = sum_df[sum_df['growth'] == sum_df['growth'].max()]
            top_growth = top_growth_row['growth'].iloc[0]
            top_variable = top_growth_row.index[0]
            return 'Top Growth', "{:,.2f}%".format(top_growth), top_variable 

    return 'Top Growth '+title, None, None

def get_pie_chart_data(df, year, chart_type):
    # Filter out rows containing certain keywords in 'variable'
    df_filtered = df[~df['variable'].str.contains('Riau|Provinsi Riau|Jumlah|Jumlah bukan makanan|Jumlah Makanan|PDRB', case=False)]
    
    if 'Jumlah' in df_filtered['turunan variable'].unique():
        df_filtered = df_filtered[df_filtered['turunan variable'] != 'Jumlah']  # Hapus kategori dengan turunan variabel 'Jumlah'

    if chart_type == 'variable':
        pie_data = df_filtered[['variable', year]].groupby('variable').sum().reset_index()
    else:  # chart_type == 'variable_turunan'
        pie_data = df_filtered[['turunan variable', year]].groupby('turunan variable').sum().reset_index()
    
    unique_turunan_var = df_filtered['turunan variable'].unique()
    return pie_data, unique_turunan_var, chart_type

# def get_pie_chart_data(df, year, chart_type):
#     df_filtered = df[~df['variable'].str.contains('Riau|Provinsi Riau|Jumlah|Jumlah bukan makanan|Jumlah Makanan|PDRB', case=False)]
    
#     if chart_type == 'variable':
#         if 'Jumlah' in df_filtered['turunan variable'].unique():
#             df_filtered = df_filtered[df_filtered['turunan variable'] != 'Jumlah']  # Hapus kategori dengan turunan variabel 'Jumlah'
#         pie_data = df_filtered[['variable', year]].groupby('variable').sum().reset_index()
#     else:  # chart_type == 'variable_turunan'
#         if 'Jumlah' in df_filtered['turunan variable'].unique():
#             df_filtered = df_filtered[df_filtered['turunan variable'] != 'Jumlah']  # Hapus kategori dengan turunan variabel 'Jumlah'
#         pie_data = df_filtered[['turunan variable', year]].groupby('turunan variable').sum().reset_index()
    
#     unique_turunan_var = df_filtered['turunan variable'].unique()
#     return pie_data, unique_turunan_var, chart_type


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


def preprocess_dataframe(df):
    if 'Jumlah' not in df['turunan variable'].unique():
        numeric_columns = df.columns[4:]
        sum_df = df.groupby(['id_var', 'variable'])[numeric_columns].sum().reset_index()
        sum_df['id_tur_var'] = 'Jumlah'
        sum_df['turunan variable'] = 'Jumlah'

        # Concatenate the original dataframe with the sum dataframe
        df = pd.concat([df, sum_df], ignore_index=True)
        
        
    return df

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

