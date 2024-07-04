import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash.dcc import Download
from dash_iconify import DashIconify
import pandas as pd
import numpy as np
from dash import dcc, html, callback, Input, Output
from dashboard import constants, common
import stadata
import dash
client = stadata.Client(constants.TOKEN)

def get_categories(df):
    categories = ['Semua Kategori'] + df['sub_name'].unique().tolist()
    initial_value = categories[0] if categories else None
    categories_menu = dmc.Select(
        data=[{'label': category, 'value': category} for category in categories],
        value=initial_value,
        placeholder="Select Category...",
        id='categories_menu',
        searchable=True,
        className="custom-dropdown",
        style=dict(width='100%')
    )
    return categories_menu

def get_sub_categories(df, selected_category):
    if selected_category == 'Semua Kategori':
        sub_categories = df['title'].unique().tolist()
    else:
        sub_categories = df[df['sub_name'] == selected_category]['title'].unique().tolist()
    initial_value = sub_categories[0] if sub_categories else None
    sub_categories_menu = dmc.Select(
        data=[{'label': sub_category, 'value': sub_category} for sub_category in sub_categories],
        value=initial_value,
        placeholder="Select Sub Category...",
        id='sub_categories_menu',
        searchable=True,
        className="custom-dropdown",
        style=dict(width='100%')
    )
    return sub_categories_menu

def get_years(df):
    years = df.columns[4:].tolist()
    current_year = str(pd.Timestamp.now().year)
    default_year = current_year if current_year in years else years[-1] if years else None
    year_dropdown = dmc.Select(
        data=[{'label': year, 'value': year} for year in years],
        value=default_year,
        placeholder="Select Year...",
        searchable=True,
        id='year_dropdown',
        className="custom-dropdown",
        style=dict(width='100%')
    )
    return year_dropdown

def province_analysis_layout():
    df = pd.read_csv(constants.CSV_FILE_DIRECTORY, encoding='ISO-8859-1')
    cat_col = get_categories(df)
    sub_cat_col = get_sub_categories(df, 'Semua Kategori')
    df_data = client.view_dynamictable(domain='1400', var=df['var_id'][0])
    df_data.iloc[:, 4:] = df_data.iloc[:, 4:].replace({'': np.nan})
    # df_data.iloc[:, 4:] = df_data.iloc[:, 4:].replace(0, np.nan)
    years_col = get_years(df_data)

    search_category_header = common.header_with_icon_div(
        icon_name='material-symbols:search-insights',
        header_text='Search Dashboard',
        icon_color='#272727',
        icon_size='1.5rem',
        header_size='1.2rem'
    )
    print(dash.__version__) 
   
    download_excel = html.Div([Download(id="download_excel")])

    download_button = dmc.Button(
        "Export to Excel", id="download_excel_button", n_clicks=0, size='xs',
        variant='outline',
        leftIcon=DashIconify(icon="ph:export-bold")
    )

    download_excel_button = html.Div([download_excel, download_button])

    options_row = dmc.Grid(
        children=[
            dmc.Col(cat_col, span=4),
            dmc.Col(sub_cat_col, span=5),
            dmc.Col(years_col, span=2),
            dmc.Col(download_excel_button, span=1)
        ],
        gutter=15,
        align='center',
        style=dict(
            width='100%',
            display='flex',
            justifyContent='space-between'
        )
    )

    search_section = dmc.CardSection(
        search_category_header,
        withBorder=True,
        inheritPadding=True,
        py='sm',
        style=dict(paddingLeft='1rem')
    )

    sub_category_card = dmc.Card(
        children=[
            search_section,
            dmc.Space(h=10),
            options_row
        ],
        withBorder=True,
        shadow="sm",
        radius="md"
    )
    sub_category_col = dmc.Col(
        [sub_category_card],
        xs=12, sm=12, md=12, lg=12, xl=12,
        style=dict()
    )

    layout = dmc.Grid(
        children=[sub_category_col],
        gutter=12,
        style=dict(paddingLeft='1.3rem', paddingRight='1.3rem')
    )

    layout = html.Div([
        layout,
        html.Div(id="dynamic-content")
    ])


    return layout
