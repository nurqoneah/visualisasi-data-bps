from provinsi.average import data_processing, plotly_visual
from dashboard import constants, common
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import pandas as pd
from dash import dcc, html

def get_summary_average(unit,df, year, vertical_id, turunan_id):
    stats_cols = []
    if unit == "Tidak Ada Satuan":
        unit =""
    elif unit == "Persen":
        unit="%"

    colors = {
        'average': constants.DASHBOARD_MAIN_COLOR1,
        'max': constants.DASHBOARD_MAIN_COLOR2,
        'min': constants.DASHBOARD_MAIN_COLOR3,
        'growth': constants.DASHBOARD_MAIN_COLOR4,
        'top_growth': constants.DASHBOARD_MAIN_COLOR5
    }

    if vertical_id != 1:
        if turunan_id == 0:
            average_title, average_df, average_desc = data_processing.get_average_change(unit,df, year, "")
            max_title, max_df, max_desc = data_processing.get_max(unit,df, year, "")
            min_title, min_df, min_desc = data_processing.get_min(unit,df, year, "")
            growth_title, growth_df = data_processing.get_growth(df, year, "")
            top_growth_title, top_growth_df, top_growth_desc = data_processing.get_top_growth(df, year, "")

            titles = [average_title, max_title, min_title, growth_title, top_growth_title]
            values = [average_df, max_df, min_df, growth_df, top_growth_df]
            descs = [average_desc, max_desc, min_desc, "", top_growth_desc]
            categories = ['average', 'max', 'min', 'growth', 'top_growth']

            icons = ['carbon:summary-kpi', 'eva:maximize-outline', 'eva:minimize-outline', 'streamline:decent-work-and-economic-growth-solid', 'uil:chart-growth-alt']
            ids = ['average', 'max', 'min', 'growth', 'top_growth']

            for title, value, desc, icon, id, category in zip(titles, values, descs, icons, ids, categories):
                div = common.content_with_icon_div(icon, colors[category], title, value, desc, id)
                card = dmc.Card(children=[div], withBorder=True, shadow="sm", radius="md")
                col = dmc.Col(children=card, xl=12 / len(ids), lg=4, md=4, sm=6, xs=6, span=5, style=dict())
                stats_cols.append(col)
        else:
            turunan_variables = df['turunan variable'].unique()

            for idx, turunan_variable in enumerate(turunan_variables):
                average_title, average_df, average_desc = data_processing.get_average_change(unit,df[df['turunan variable'] == turunan_variable], year, turunan_variable)

                titles = [average_title]
                values = [average_df]
                descs = [average_desc]
                categories = ['average']

                icons = ['carbon:summary-kpi']
                ids = ['average{}'.format(idx)]

                for title, value, desc, icon, id, category in zip(titles, values, descs, icons, ids, categories):
                    div = common.content_with_icon_div(icon, colors[category], title, value, desc, id)
                    card = dmc.Card(children=[div], withBorder=True, shadow="sm", radius="md")
                    col = dmc.Col(children=card, xl=4, lg=4, md=4, sm=6, xs=6, span=5, style=dict())
                    stats_cols.append(col)
    else:
        average_title, average_df, average_desc = data_processing.get_average_change(unit,df, year, "")
        div = common.content_with_icon_div('carbon:summary-kpi', colors['average'], average_title, average_df, average_desc, "average")
        card = dmc.Card(children=[div], withBorder=True, shadow="sm", radius="md")
        col = dmc.Col(children=card, xl=12/3, lg=4, md=4, sm=6, xs=6, span=5, style=dict())
        stats_cols.append(col)

    return stats_cols

def get_bar_chart_col(unit,selected_value,df, year, turunan_id):
    if turunan_id != 0:
      
        rotated_bar_fig = plotly_visual.get_rotated_bar_chart(data_processing.get_filter_df(df), year)

        bar_chart_graph = dcc.Graph(
            figure=rotated_bar_fig,
            config={'displaylogo': False, 'modeBarButtonsToRemove': ['lasso2d', 'pan']},
            id='avg_bar_chart_fig',
            className='bar_chart_graph',
            style=dict(width='', height='500px')
        )

        bar_chart_header = common.header_with_icon_div(
            icon_name='ion:bar-chart-sharp',
            header_text='Bar Chart '+selected_value+" "+year+" "+unit,
            icon_color='#272727',
            icon_size='1.5rem',
            header_size='1.2rem'
        )

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
    else:
       
        bar_chart_data, _, _ = data_processing.get_bar_chart_data(df, year, 'variable')
        bar_chart_fig = plotly_visual.get_bar_chart_figure(bar_chart_data, year, 'variable')
        bar_chart_graph = dcc.Graph(
            figure=bar_chart_fig,
            config={'displaylogo': False, 'modeBarButtonsToRemove': ['lasso2d', 'pan']},
            id='avg_bar_chart_fig',
            className='bar_chart_graph',
            style=dict(width='', height='500px') 
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
                id='avg_turunan_variabel_dropdown_heatmap',
                style=dict(maxWidth='40%', display='block', height='49.8px'),
            )
        else:
            dropdown_value = turunan_variabel[0]
            option_turunan_variable = dmc.Select(
                data=[{'label': var, 'value': var} for var in turunan_variabel],
                value=dropdown_value,
                searchable=True,
                clearable=False,
                id='avg_turunan_variabel_dropdown_heatmap',
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
        id='avg_heatmap_fig',
        className='pie_chart_graph',
        style=dict(width='', height='')
    )


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
            id='avg_turunan_variabel_dropdown_time_series',
            style=dict(maxWidth='40%', display='block')
        )
    else:
        dropdown_value = turunan_variabel[0]
        option_turunan_variable = dmc.Select(
            value=dropdown_value,
            id='avg_turunan_variabel_dropdown_time_series',
            style=dict(maxWidth='40%', display='none')
        )

        
    variables = df['variable'].unique().tolist()
    selected_variables = [variables[0]] 

    option_variables = dmc.MultiSelect(
        data=[{'label': var, 'value': var} for var in variables],
        value=selected_variables,
        id='avg_variables_multi_select',
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

    time_series_fig = plotly_visual.get_time_series_figure(data_processing.get_time_series_data(df, dropdown_value, selected_variables)) 

    time_series_graph = dcc.Graph(
        figure=time_series_fig,
        config={'displaylogo': False, 'modeBarButtonsToRemove': ['lasso2d', 'pan']},
        id='avg_time_series_fig',
        className='time_series_graph',
        style=dict(width='', height='')
    )
    time_series_graph = dbc.Spinner([time_series_graph], size="lg", color="primary", type="border", fullscreen=False)

    time_series_card = dmc.Card(
        children=[
            dmc.CardSection(common.header_with_icon_div(icon_name='grommet-icons:time',
                                                         header_text='Time Series '+selected_value+" "+unit,
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

def get_scatter_plot_col(unit,selected_value,df, year):
    scatter_plot_fig = plotly_visual.get_scatter_plot_figure(data_processing.get_scatter_plot_data(df, year),year)

    scatter_plot_graph = dcc.Graph(
        figure=scatter_plot_fig,
        config={'displaylogo': False, 'modeBarButtonsToRemove': ['lasso2d', 'pan']},
        id='avg_scatter_plot_fig',
        className='scatter_plot_graph',
        style=dict(width='', height='500px')  
    )
    scatter_plot_graph = dbc.Spinner([scatter_plot_graph], size="lg", color="primary", type="border", fullscreen=False)
    scatter_plot_card=dmc.Card(
            children=[
                dmc.CardSection(common.header_with_icon_div(icon_name='grommet-icons:time',
                                                            header_text='Scatter Plot '+selected_value+" "+year+" "+unit,
                                                            icon_color='#272727',
                                                            icon_size='1.5rem',
                                                            header_size='1.2rem'
                                                            ),
                                withBorder=True, inheritPadding=True, py='sm',
                                style={'paddingLeft': '1rem'}),
                dmc.Space(h=7),
            
                scatter_plot_graph
            ],
            withBorder=True,
            shadow="sm",
            radius="md"
        )

    scatter_plot_col = dmc.Col(
        [scatter_plot_card],
        xs=12, sm=12, md=6, lg=6, xl=6,
        style=dict()
    )


    return scatter_plot_col

def average_analysis_layout(unit,selected_value, df, year, vertical_id, turunan_id):
    if unit == "Tidak Ada Satuan":
        units=""
    else:
        units="("+unit+")"
    years = df.columns[4:].tolist()
    years_count = len(years)
    
    layout_item =[]

    if vertical_id != 1:
        pie_chart_col = get_scatter_plot_col(units,selected_value,df, year)
        layout_item.append(pie_chart_col)
        heatmap_layout = get_heatmap_layout(units,selected_value,df,year,vertical_id)
        layout_item.append(heatmap_layout)
        bar_chart_layout = get_bar_chart_col(units,selected_value,df,year, turunan_id)
        layout_item.append(bar_chart_layout)
        if years_count>1:
            time_series_chart_layout = get_time_series_layout(units,selected_value,df)
            layout_item.append(time_series_chart_layout)
        
        
    else:
        
        if years_count>1:
            time_series_chart_layout = get_time_series_layout(units,selected_value,df)
        layout_item.append(time_series_chart_layout)


    stats_cols = get_summary_average(unit,df, year,vertical_id, turunan_id)

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


