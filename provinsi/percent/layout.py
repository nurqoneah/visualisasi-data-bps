from provinsi.percent import data_processing, plotly_visual
from dashboard import constants, common
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import pandas as pd
from dash import dcc, html

def get_percent_sum(unit, df, year, turunan_id):
    if unit == "Tidak Ada Satuan":
        unit =""
    elif unit == "Persen":
        unit="%"
    
    stats_cols = []

    colors = {
        'max': constants.DASHBOARD_MAIN_COLOR2,
        'min': constants.DASHBOARD_MAIN_COLOR3,
    }

    if turunan_id == 0:
        max_title, max_df, max_desc = data_processing.get_max(unit, df, year, "")
        min_title, min_df, min_desc = data_processing.get_min(unit, df, year, "")

        titles = [max_title, min_title]
        values = [max_df, min_df]
        descs = [max_desc, min_desc]
        categories = ['max', 'min']

        icons = ['eva:maximize-outline', 'eva:minimize-outline']
        ids = ['max1', 'min1']

        for title, value, desc, icon, id, category in zip(titles, values, descs, icons, ids, categories):
            div = common.content_with_icon_div(icon, colors[category], title, value, desc, id)
            card = dmc.Card(children=[div], withBorder=True, shadow="sm", radius="md")
            col = dmc.Col(children=card, xl=12 / len(ids), lg=6, md=6, sm=6, xs=6, span=5, style=dict())
            stats_cols.append(col)

    elif turunan_id == 1:
        turunan_variables = df['turunan variable'].unique()

        for idx, turunan_variable in enumerate(turunan_variables):
            max_title, max_df, max_desc = data_processing.get_max(unit,df[df['turunan variable'] == turunan_variable], year, turunan_variable)
            min_title, min_df, min_desc = data_processing.get_min(unit,df[df['turunan variable'] == turunan_variable], year, turunan_variable)

            titles = [max_title, min_title]
            values = [max_df, min_df]
            descs = [max_desc, min_desc]
            categories = ['max', 'min']

            icons = ['eva:maximize-outline', 'eva:minimize-outline']
            ids = ['max{}'.format(idx), 'min{}'.format(idx)]

            for title, value, desc, icon, id, category in zip(titles, values, descs, icons, ids, categories):
                div = common.content_with_icon_div(icon, colors[category], title, value, desc, id)
                card = dmc.Card(children=[div], withBorder=True, shadow="sm", radius="md")
                col = dmc.Col(children=card, xl=12 / len(ids), lg=6, md=6, sm=6, xs=6, span=5, style=dict())
                stats_cols.append(col)

    return stats_cols

def get_pie_chart_col(unit,selected_value,df, year, turunan_id):
    chart_type_options = None
    options_row = None

    if turunan_id != 0:
        chart_types = [ ['Sunburst Chart', 'sunburst_chart'], ['Pie Chart', 'pie_chart'],]
        chart_type_options = dmc.RadioGroup(
            children=[dmc.Radio(l, value=v) for l, v in chart_types],
            value='sunburst_chart',
            id="percent_chart_type_options",
            label="Chart Type",
            size="xs",
            mt=5,
            offset=4
        )

        chart_type = chart_type_options.value
        pie_chart_data = data_processing.get_filter_df(df)

        if chart_type == 'pie_chart':
            pie_chart_fig = plotly_visual.get_mul_pie_chart_figure(pie_chart_data, year)
            pie_chart_graph = dcc.Graph(
                figure=pie_chart_fig,
                config={'displaylogo': False, 'modeBarButtonsToRemove': ['lasso2d', 'pan']},
                id='percent_pie_chart_fig',
                className='pie_chart_graph',
                style=dict(width='', height='450px')  # Fixed height for single chart
            )
        else:
            sunburst_fig = plotly_visual.get_sunburst_chart_figure(data_processing.get_filter_df(df), year)
            pie_chart_graph = dcc.Graph(
                figure=sunburst_fig,
                config={'displaylogo': False, 'modeBarButtonsToRemove': ['lasso2d', 'pan']},
                id='percent_pie_chart_fig',
                className='sunburst_chart_graph',
                style=dict(width='', height='450px')  # Fixed height for single chart
            )

        pie_chart_graph = dcc.Loading(
            [pie_chart_graph], 
            color="primary", 
            type="border", 
            fullscreen=False, 
            custom_spinner=html.Div([
                dmc.Loader(color=constants.MAIN_HEADER_BG, variant="bars", size="md"),
                html.H2("Load Visualisasi", style={"font-size": "0.7rem", "margin-top": "0.3rem"})
            ])
        )

        pie_chart_header = common.header_with_icon_div(
            icon_name='ion:pie-chart',
            header_text='Pie Chart '+selected_value+" "+year+" "+unit,
            icon_color='#272727',
            icon_size='1.5rem',
            header_size='1.2rem'
        )

        options_row = dmc.Group(
            children=[chart_type_options],
            spacing=15,
            align='center',
            position='left'
        )
        pie_chart_graph = dbc.Spinner([pie_chart_graph], size="lg", color="primary", type="border", fullscreen=False)

        pie_chart_card = dmc.Card(
            children=[
                dmc.CardSection(pie_chart_header, withBorder=True, inheritPadding=True, py='sm', style={'paddingLeft': '1rem'}),
                dmc.Space(h=7),
                options_row,
                pie_chart_graph
            ],
            withBorder=True,
            shadow="sm",
            radius="md"
        )

        pie_chart_col = dmc.Col(
            [pie_chart_card],
            xs=12, sm=12, md=6, lg=6, xl=6,
            style=dict()
        )
        return pie_chart_col

    else:
        pie_chart_fig = plotly_visual.get_pie_chart_figure(data_processing.get_filter_df(df), year)

        pie_chart_graph = dcc.Graph(
            figure=pie_chart_fig,
            config={'displaylogo': False, 'modeBarButtonsToRemove': ['lasso2d', 'pan']},
            id='percent_pie_chart_fig',
            className='pie_chart_graph',
            style=dict(width='', height='500px')
        )

        pie_chart_graph = dbc.Spinner([pie_chart_graph], size="lg", color="primary", type="border", fullscreen=False)

        pie_chart_header = common.header_with_icon_div(
            icon_name='ion:pie-chart',
            header_text='Pie Chart '+selected_value+" "+year+" "+unit,
            icon_color='#272727',
            icon_size='1.5rem',
            header_size='1.2rem'
        )

        pie_chart_card = dmc.Card(
            children=[
                dmc.CardSection(pie_chart_header, withBorder=True, inheritPadding=True, py='sm', style={'paddingLeft': '1rem'}),
                dmc.Space(h=7),
                pie_chart_graph
            ],
            withBorder=True,
            shadow="sm",
            radius="md"
        )

        pie_chart_col = dmc.Col(
            [pie_chart_card],
            xs=12, sm=12, md=6, lg=6, xl=6,
            style=dict()
        )

        return pie_chart_col

def get_bar_chart_col(unit,selected_value,df, year, turunan_id):
    bar_chart_fig = plotly_visual.get_stacked_bar_chart_figure(data_processing.get_filter_df(df), year, turunan_id)

    bar_chart_graph = dcc.Graph(
        figure=bar_chart_fig,
        config={'displaylogo': False, 'modeBarButtonsToRemove': ['lasso2d', 'pan']},
        id='percent_bar_chart_fig',
        className='bar_chart_graph',
        style=dict(width='', height='500px')  # Fixed height for single chart
    )

    bar_chart_header = common.header_with_icon_div(
        icon_name='ion:bar-chart-sharp',
        header_text='Bar Chart '+selected_value+" "+year+" "+unit,
        icon_color='#272727',
        icon_size='1.5rem',
        header_size='1.2rem'
    )
    bar_chart_graph = dbc.Spinner([bar_chart_graph], size="lg", color="primary", type="border", fullscreen=False)
    
    bar_chart_card = dmc.Card(
        children=[
            dmc.CardSection(bar_chart_header, withBorder=True, inheritPadding=True, py='sm', style={'paddingLeft': '1rem'}),
            dmc.Space(h=7),
            bar_chart_graph
        ],
        withBorder=True,
        shadow="sm",
        radius="md"
    )

    bar_chart_col = dmc.Col(
        [bar_chart_card],
        xs=12, sm=12, md=6, lg=6, xl=6,
        style=dict()
    )

    return bar_chart_col

def get_heatmap_layout(unit,selected_value,df, year, vertical_id):
    if vertical_id in [6, 7]:
        turunan_variabel = df['turunan variable'].unique().tolist()
        dropdown_value = turunan_variabel[0]
        
        heatmap_fig = plotly_visual.get_heatmap_geos_figure(data_processing.get_heatmap_data(df, year, dropdown_value), year)
    else:
        heatmap_fig = plotly_visual.get_heatmap_figure(data_processing.get_filter_df(df), year)

    heatmap_graph = dcc.Graph(
        figure=heatmap_fig,
        config={'displaylogo': False, 'modeBarButtonsToRemove': ['lasso2d', 'pan']},
        id='percent_heatmap_fig',
        className='pie_chart_graph',
        style=dict(width='', height='500px')
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
    df = data_processing.get_filter_df(df)
    area_chart_fig = plotly_visual.get_area_chart_figure(df)

    area_chart_graph = dcc.Graph(
        figure=area_chart_fig,
        config={'displaylogo': False, 'modeBarButtonsToRemove': ['lasso2d', 'pan']},
        id='percent_area_chart_fig',
        className='area_chart_graph',
        style=dict(width='', height='500px')  # Fixed height for single chart
    )

    area_chart_header = common.header_with_icon_div(icon_name='carbon:heat-map-03',
                                                 header_text='Area Chart '+selected_value+" "+unit,
                                                 icon_color='#272727',
                                                 icon_size='1.5rem',
                                                 header_size='1.2rem'
                                                 )
    
    area_chart_graph = dbc.Spinner([area_chart_graph], size="lg", color="primary", type="border", fullscreen=False)

    area_chart_card = dmc.Card(
        children=[
            dmc.CardSection(area_chart_header, withBorder=True, inheritPadding=True, py='sm',
                             style={'paddingLeft': '1rem'}),
            dmc.Space(h=7),
            area_chart_graph
        ],
        withBorder=True,
        shadow="sm",
        radius="md"
    )

    area_chart_col = dmc.Col(
        [area_chart_card],
        xs=12, sm=12, md=6, lg=6, xl=6,
        style=dict()
    )

    return area_chart_col

def percent_analysis_layout(unit, selected_value, df, year, vertical_id, turunan_id):
    if unit == "Tidak Ada Satuan":
        units=""
    else:
        units="("+unit+")"
    years = df.columns[4:].tolist()
    years_count = len(years)
    print(year)
    layout_item =[]

    if turunan_id == 0:
        pie_chart_col = get_pie_chart_col(units,selected_value,df, year, turunan_id)
        layout_item.append(pie_chart_col)
        heatmap_layout = get_heatmap_layout(units,selected_value,df,year,vertical_id)
        layout_item.append(heatmap_layout)
        bar_chart_layout = get_bar_chart_col(units,selected_value,df,year, turunan_id)
        layout_item.append(bar_chart_layout)
        if years_count>1:
            df = df[~df['variable'].str.contains('Riau|Provinsi Riau|Jumlah|Jumlah bukan makanan|Jumlah Makanan|PDRB', case=False)]
            time_series_chart_layout = get_time_series_layout(units,selected_value,df)
            layout_item.append(time_series_chart_layout)
        
        
    else:
        pie_chart_col = get_pie_chart_col(units,selected_value,df, year, turunan_id)
        layout_item.append(pie_chart_col)
        bar_chart_layout = get_bar_chart_col(units,selected_value,df,year, turunan_id)
        layout_item.append(bar_chart_layout)
        

    stats_cols = get_percent_sum(unit, df, year, turunan_id)

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


