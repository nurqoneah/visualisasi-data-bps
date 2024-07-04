from provinsi.other import data_processing, plotly_visual
from dashboard import constants, common
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import dcc, html

def get_summary_other(unit, df, year, turunan_id):
    stats_cols = []
    if unit == "Tidak Ada Satuan":
        unit =""

    elif unit == "Persen":
        unit="%"

    colors = {
        'max': constants.DASHBOARD_MAIN_COLOR2,
        'min': constants.DASHBOARD_MAIN_COLOR3,
    }

    if turunan_id == 0|3:
        max_title, max_df, max_desc = data_processing.get_max(unit, df, year, "")
        min_title, min_df, min_desc = data_processing.get_min(unit, df, year, "")

        titles = [max_title, min_title]
        values = [max_df, min_df]
        descs = [max_desc, min_desc]
        categories = ['max', 'min']

        icons = ['eva:maximize-outline', 'eva:minimize-outline']
        ids = ['max', 'min']

        for title, value, desc, icon, id, category in zip(titles, values, descs, icons, ids, categories):
            div = common.content_with_icon_div(icon, colors[category], title, value, desc, id)
            card = dmc.Card(children=[div], withBorder=True, shadow="sm", radius="md")
            col = dmc.Col(children=card, xl=12 / len(ids), lg=6, md=6, sm=6, xs=6, span=5, style=dict())
            stats_cols.append(col)

    else:
        turunan_variables = df['turunan variable'].unique()

        for idx, turunan_variable in enumerate(turunan_variables):
            max_title, max_df, max_desc = data_processing.get_max(unit,df[df['turunan variable'] == turunan_variable], year, turunan_variable)
            min_title, min_df, min_desc = data_processing.get_min(unit,df[df['turunan variable'] == turunan_variable], year, turunan_variable)

            titles = [max_title, min_title]
            values = [max_df, min_df]
            descs = [max_desc, min_desc]
            categories = ['max', 'min']

            icons = ['eva:maximize-outline', 'eva:minimize-outline']
            ids = ['max', 'min']

            for title, value, desc, icon, id, category in zip(titles, values, descs, icons, ids, categories):
                div = common.content_with_icon_div(icon, colors[category], title, value, desc, id)
                card = dmc.Card(children=[div], withBorder=True, shadow="sm", radius="md")
                col = dmc.Col(children=card, xl=12 / len(ids), lg=6, md=6, sm=6, xs=6, span=5, style=dict())
                stats_cols.append(col)

    return stats_cols

def get_heatmap_layout(unit,selected_value, df, year, vertical_id):
    if vertical_id in [6, 7, 50]:
        turunan_variabel = df['turunan variable'].unique().tolist()

        if len(turunan_variabel) > 1:
            if 'Jumlah' in turunan_variabel:
                turunan_variabel.remove('Jumlah')
                turunan_variabel.insert(0, 'Jumlah')
            dropdown_value = turunan_variabel[0]
            option_turunan_variable = dmc.Select(
                data=[{'label': var, 'value': var} for var in turunan_variabel],
                value=dropdown_value,
                searchable=True,
                clearable=False,
                id='sum_turunan_variabel_dropdown_heatmap',
                style=dict(maxWidth='40%', display='block', height='49.8px'),
            )
        else:
            dropdown_value = turunan_variabel[0]
            option_turunan_variable = dmc.Select(
                data=[{'label': var, 'value': var} for var in turunan_variabel],
                value=dropdown_value,
                searchable=True,
                clearable=False,
                id='sum_turunan_variabel_dropdown_heatmap',
                style=dict(maxWidth='40%', display='none', height='49.8px'),
            )

        options1_row = dmc.Group(
            children=[option_turunan_variable],
            spacing=15,
            align='center',
            position='left',
            style=dict(height='49.8px', paddingTop='10px')
        )
        
        heatmap_fig = plotly_visual.get_heatmap_geos_figure(data_processing.get_heatmap_data(df, year, dropdown_value), year)
    else:
       
        options1_row = dmc.Group(
            children=[],
            spacing=15,
            align='center',
            position='left',
            style=dict(height='49.8px', paddingTop='10px',)
        )

        heatmap_fig = plotly_visual.get_heatmap_figure(data_processing.get_filter_df(df), year)

    heatmap_graph = dcc.Graph(
        figure=heatmap_fig,
        config={'displaylogo': False, 'modeBarButtonsToRemove': ['lasso2d', 'pan']},
        id='sum_heatmap_fig',
        className='pie_chart_graph',
        style=dict(width='', height='')
    )

    # heatmap_graph = dbc.Spinner([heatmap_graph], size="lg", color="primary", type="border", fullscreen=False)

    heatmap_header = common.header_with_icon_div(icon_name='carbon:heat-map-03',
                                                 header_text='Heatmap '+selected_value+" "+year+" "+unit,
                                                 icon_color='#272727',
                                                 icon_size='1.5rem',
                                                 header_size='1.2rem'
                                                 )
    heatmap_graph = dbc.Spinner([heatmap_graph], size="lg", color="primary", type="border", fullscreen=False)
    heatmap_card = dmc.Card(
        children=[
            dmc.CardSection(heatmap_header, withBorder=True, inheritPadding=True, py='sm',
                             style={'paddingLeft': '1rem'}),
            dmc.Space(h=7),
            options1_row,
            heatmap_graph
        ],
        withBorder=True,
        shadow="sm",
        radius="md"
    )

    heatmap_col = dmc.Col(
        [heatmap_card],
        xs=12, sm=12, md=6, lg=6, xl=6,
        style=dict()
    )

    return heatmap_col

def get_time_series_layout(unit,selected_value,df):
    # df=data_processing.preprocess_dataframe(df)
    turunan_variabel = df['turunan variable'].unique().tolist()
    

    # Dropdown for selecting turunan variabel
    if len(turunan_variabel) > 1:
        if 'Jumlah' in turunan_variabel:
            turunan_variabel.remove('Jumlah')
            turunan_variabel.insert(0, 'Jumlah')
        dropdown_value = turunan_variabel[0]  

        option_turunan_variable = dmc.Select(
            data=[{'label': var, 'value': var} for var in turunan_variabel],
            value=dropdown_value,
            searchable=True,
            clearable=False,
            id='sum_turunan_variabel_dropdown_time_series',
            style=dict(maxWidth='40%', display='block')
        )
    else:
        dropdown_value = turunan_variabel[0]
        option_turunan_variable = dmc.Select(
            value=dropdown_value,
            id='sum_turunan_variabel_dropdown_time_series',
            style=dict(maxWidth='40%', display='none')
        )

        
    variables = df['variable'].unique().tolist()
    selected_variables = [variables[0]]  # default selected variables

    option_variables = dmc.MultiSelect(
        data=[{'label': var, 'value': var} for var in variables],
        value=selected_variables,
        id='sum_variables_multi_select',
        className='multiselect_ts',
        style=dict(height='100%')
    )
    

    options_row = dmc.Group(
        children=[option_turunan_variable, option_variables],
        spacing=15,
        align='center',
        position='left',
        style=dict(height='49.8px', paddingTop='10px')
    )

    time_series_fig = plotly_visual.get_time_series_figure(data_processing.get_time_series_data(df, dropdown_value, selected_variables))  # assuming you have a function to generate time series figure

    time_series_graph = dcc.Graph(
        figure=time_series_fig,
        config={'displaylogo': False, 'modeBarButtonsToRemove': ['lasso2d', 'pan']},
        id='sum_time_series_fig',
        className='time_series_graph',
        style=dict(width='', height='')
    )

    time_series_graph = dbc.Spinner([time_series_graph], size="lg", color="primary", type="border", fullscreen=False)

    time_series_card = dmc.Card(
        children=[
            dmc.CardSection(common.header_with_icon_div(icon_name='grommet-icons:time',
                                                         header_text='Time Series '+selected_value+" "+ unit,
                                                         icon_color='#272727',
                                                         icon_size='1.5rem',
                                                         header_size='1.2rem'
                                                         ),
                            withBorder=True, inheritPadding=True, py='sm',
                            style={'paddingLeft': '1rem'}),
            dmc.Space(h=7),
            options_row,
            time_series_graph
        ],
        withBorder=True,
        shadow="sm",
        radius="md"
    )

    time_series_col = dmc.Col(
        [time_series_card],
        xs=12, sm=12, md=6, lg=6, xl=6,
        style=dict()
    )

    return time_series_col

def other_analysis_layout(unit, selected_value,df, year, vertical_id, turunan_id, sub_id):
    if unit == "Tidak Ada Satuan":
        units=""
    else:
        units="("+unit+")"
    years = df.columns[4:].tolist()
    years_count = len(years)
    print(year)
    layout_item =[]
    if sub_id!=30:
        df=df[df["turunan variable"]=="Tidak Ada"]
        stats_cols = get_summary_other(unit, df, year, turunan_id)
    else:
        stats_cols =[]


    if years_count>1:
        time_series_chart_layout = get_time_series_layout(units,selected_value, df)
    layout_item.append(time_series_chart_layout)

    
    heatmap_layout = get_heatmap_layout(units,selected_value, df,year, vertical_id)
    layout_item.append(heatmap_layout)

    
    

    stats_div = dmc.Grid(
        stats_cols,
        align="center",
        justify="space-around",
        gutter="md",
        style=dict(marginTop='.5rem', paddingLeft='1.5rem', paddingRight='1.5rem')
    )
    
    layout = html.Div(
        [stats_div,
         dmc.Space(h=15),
         dmc.Grid(layout_item, align="center",
        justify="space-around",gutter=12, style=dict(paddingLeft='1.3rem', paddingRight='1.3rem')),
         dmc.Space(h=20)],
         
    )
    
    return layout


