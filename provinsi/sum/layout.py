from provinsi.sum import data_processing, plotly_visual
from dashboard import constants, common
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import dcc, html

def get_summary_sum(unit, df, year, vertical_id, turunan_id):
    stats_cols = []
    if unit == "Tidak Ada Satuan":
        unit =""
    elif unit == "Persen":
        unit="%"

    colors = {
        'total': constants.DASHBOARD_MAIN_COLOR1,
        'max': constants.DASHBOARD_MAIN_COLOR2,
        'min': constants.DASHBOARD_MAIN_COLOR3, 
        'growth': constants.DASHBOARD_MAIN_COLOR4,  
        'top_growth': constants.DASHBOARD_MAIN_COLOR5  
    }

    if vertical_id != 1:
        if turunan_id != 2:
            total_title, total_df, total_desc = data_processing.get_total_change(unit,df, year, "")
            max_title, max_df, max_desc = data_processing.get_max(unit, df, year, "")
            min_title, min_df, min_desc = data_processing.get_min(unit, df, year, "")

            titles = [total_title, max_title, min_title]
            values = [total_df, max_df, min_df]
            descs = [total_desc, max_desc, min_desc]
            categories = ['total', 'max', 'min']

            icons = ['carbon:summary-kpi', 'eva:maximize-outline', 'eva:minimize-outline']
            ids = ['total', 'max', 'min']

            for title, value, desc, icon, id, category in zip(titles, values, descs, icons, ids, categories):
                div = common.content_with_icon_div(icon, colors[category], title, value, desc, id)
                card = dmc.Card(children=[div], withBorder=True, shadow="sm", radius="md")
                col = dmc.Col(children=card, xl=12 / len(ids), lg=4, md=4, sm=6, xs=6, span=5, style=dict())
                stats_cols.append(col)
        else:
            turunan_variables = df['turunan variable'].unique()
            
            for idx, turunan_variable in enumerate(turunan_variables):
                total_title, total_df, total_desc = data_processing.get_total_change(unit, df[df['turunan variable'] == turunan_variable], year, turunan_variable)
                max_title, max_df, max_desc = data_processing.get_max(unit, df[df['turunan variable'] == turunan_variable], year, turunan_variable)
                min_title, min_df, min_desc = data_processing.get_min(unit,df[df['turunan variable'] == turunan_variable], year, turunan_variable)

                titles = [total_title, max_title, min_title]
                values = [total_df, max_df, min_df]
                descs = [total_desc, max_desc, min_desc]
                categories = ['total', 'max', 'min']

                icons = ['carbon:summary-kpi', 'eva:maximize-outline', 'eva:minimize-outline']
                ids = ['total', 'max', 'min']

                for title, value, desc, icon, id, category in zip(titles, values, descs, icons, ids, categories):
                    div = common.content_with_icon_div(icon, colors[category], title, value, desc, id)
                    card = dmc.Card(children=[div], withBorder=True, shadow="sm", radius="md")
                    col = dmc.Col(children=card, xl=12 / len(ids), lg=4, md=4, sm=6, xs=6, span=5, style=dict())
                    stats_cols.append(col)

        if vertical_id in [6, 7, 8, 9, 14, 15, 18, 22, 23, 27, 30, 31, 42]:
            if turunan_id != 2:
                growth_title, growth_df = data_processing.get_growth(df, year, "Growth")
                top_growth_title, top_growth_df, top_growth_desc = data_processing.get_top_growth(df, year, "Top Growth")

                titles = [growth_title, top_growth_title]
                values = [growth_df, top_growth_df]
                descs = ["", top_growth_desc]
                categories = ['growth', 'top_growth']

                icons = ['streamline:decent-work-and-economic-growth-solid', 'uil:chart-growth-alt']
                ids = ['growth', 'top_growth']

                for title, value, desc, icon, id, category in zip(titles, values, descs, icons, ids, categories):
                    div = common.content_with_icon_div(icon, colors[category], title, value, desc, id)
                    card = dmc.Card(children=[div], withBorder=True, shadow="sm", radius="md")
                    col = dmc.Col(children=card, xl=12 / len(ids), lg=4, md=4, sm=6, xs=6, span=5, style=dict())
                    stats_cols.append(col)
            else:
                turunan_variables = df['turunan variable'].unique()
                for idx, turunan_variable in enumerate(turunan_variables):
                    growth_title, growth_df = data_processing.get_growth(df[df['turunan variable'] == turunan_variable], year, turunan_variable)
                    top_growth_title, top_growth_df, top_growth_desc = data_processing.get_top_growth(df[df['turunan variable'] == turunan_variable], year, turunan_variable)

                    titles = [growth_title, top_growth_title]
                    values = [growth_df, top_growth_df]
                    descs = ["", top_growth_desc]
                    categories = ['growth', 'top_growth']

                    icons = ['streamline:decent-work-and-economic-growth-solid', 'uil:chart-growth-alt']
                    ids = ['growth', 'top_growth']

                    for title, value, desc, icon, id, category in zip(titles, values, descs, icons, ids, categories):
                        div = common.content_with_icon_div(icon, colors[category], title, value, desc, id)
                        card = dmc.Card(children=[div], withBorder=True, shadow="sm", radius="md")
                        col = dmc.Col(children=card, xl=12 / len(ids), lg=4, md=4, sm=6, xs=6, span=5, style=dict())
                        stats_cols.append(col)
    else:
        total_title, total_df, total_desc = data_processing.get_total_change(unit,df, year, "")
        div = common.content_with_icon_div('carbon:summary-kpi', colors['total'], total_title, total_df, total_desc, "total1")
        card = dmc.Card(children=[div], withBorder=True, shadow="sm", radius="md")
        col = dmc.Col(children=card, xl=12/3, lg=4, md=4, sm=6, xs=6, span=5, style=dict())
        stats_cols.append(col)

    return stats_cols

def get_pie_chart_col(unit,selected_value,df, year, turunan_id):
    chart_type_options = None
    value_type_options = None
    options_row = None  

    if turunan_id != 2:
        if turunan_id == 0:
            pie_chart_data, unique_turunan_var, value_type = data_processing.get_pie_chart_data(df, year, 'variable')
            pie_chart_fig = plotly_visual.get_pie_chart_figure(pie_chart_data, year, 'variable')
            pie_chart_graph = dcc.Graph(
                figure=pie_chart_fig,
                config={'displaylogo': False, 'modeBarButtonsToRemove': ['lasso2d', 'pan']},
                id='sum_pie_chart_fig',
                className='pie_chart_graph',
                style=dict(width='', height='500px')  # Fixed height for single chart
            )
        else:
            chart_types = [['Pie Chart', 'pie_chart'], ['Sunburst Chart', 'sunburst_chart']]
            chart_type_options = dmc.RadioGroup(
                children=[dmc.Radio(l, value=v) for l, v in chart_types],
                value='pie_chart',
                id="sum_chart_type_options",
                label="Chart Type",
                size="xs",
                mt=5,
                offset=4
            )
            
            
            chart_type = chart_type_options.value
            
            pie_chart_data, unique_turunan_var, value_type = data_processing.get_pie_chart_data(df, year, 'variable')

            value_types = [['Variable', 'variable']]
            if not (len(unique_turunan_var) == 1 and unique_turunan_var[0] == 'Tidak Ada'):
                value_types.append(['Turunan Variabel', 'turunan variable'])  # Ensure name matches the DataFrame

            value_type_options = dmc.RadioGroup(
                children=[dmc.Radio(l, value=v) for l, v in value_types],
                value='variable',
                id="sum_value_type_options",
                label="Value Type",
                size="xs",
                mt=5,
                offset=4
            )

            options_row = dmc.Group(
                children=[chart_type_options, value_type_options],
                spacing=15,
                align='center',
                position='left'
            )

            if chart_type == 'pie_chart':
                pie_chart_fig = plotly_visual.get_pie_chart_figure(pie_chart_data, year, value_type)

                pie_chart_graph = dcc.Graph(
                    figure=pie_chart_fig,
                    config={'displaylogo': False, 'modeBarButtonsToRemove': ['lasso2d', 'pan']},
                    id='sum_pie_chart_fig',
                    className='pie_chart_graph',
                    style=dict(width='', height='450px')  # Fixed height for single chart
                )

            else:  # Sunburst chart
                if value_type == 'variable':
                    sunburst_fig = plotly_visual.get_sunburst_chart_figure(data_processing.get_filter_df(df), year, path=['variable', 'turunan variable'])
                else:
                    sunburst_fig = plotly_visual.get_sunburst_chart_figure(data_processing.get_filter_df(df), year, path=['turunan variable', 'variable'])

                pie_chart_graph = dcc.Graph(
                    figure=sunburst_fig,
                    config={'displaylogo': False, 'modeBarButtonsToRemove': ['lasso2d', 'pan']},
                    id='sum_pie_chart_fig',
                    className='sunburst_chart_graph',
                    style=dict(width='', height='450px')  # Fixed height for single chart
                )
                

        # pie_chart_graph = dcc.Loading([pie_chart_graph],  color="primary", type="border", fullscreen=False, custom_spinner=html.Div([
        #             dmc.Loader(color=constants.MAIN_HEADER_BG, variant="bars",size="md",  ),
        #             html.H2("Load Visualisasi", style={"font-size": "0.7rem", "margin-top": "0.3rem" })
        #     ]))
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
                options_row if options_row else dmc.Space(),  # Ensure options_row is not None
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
        pie_chart_fig = plotly_visual.get_mul_pie_chart_figure(df, year)

        pie_chart_graph = dcc.Graph(
            figure=pie_chart_fig,
            config={'displaylogo': False, 'modeBarButtonsToRemove': ['lasso2d', 'pan']},
            id='sum_pie_chart_fig',
            className='pie_chart_graph',
            style=dict(width='', height='500px')
        )

        pie_chart_graph = dbc.Spinner([pie_chart_graph], size="lg", color="primary", type="border", fullscreen=False)

        pie_chart_header = common.header_with_icon_div(
            icon_name='vion:pie-chart',
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
    chart_type_options_bar = None
    value_type_options_bar = None
    options_row = None  # Initialize options_row to avoid UnboundLocalError

    if turunan_id != 2:
        if turunan_id == 0:
            bar_chart_data, unique_turunan_var, value_type = data_processing.get_bar_chart_data(df, year, 'variable')
            bar_chart_fig = plotly_visual.get_bar_chart_figure(bar_chart_data, year, 'variable')
            bar_chart_graph = dcc.Graph(
                figure=bar_chart_fig,
                config={'displaylogo': False, 'modeBarButtonsToRemove': ['lasso2d', 'pan']},
                id='sum_bar_chart_fig',
                className='bar_chart_graph',
                style=dict(width='', height='500px')  # Fixed height for single chart
            )
        else:
            # Options for chart type
            chart_types = [['Bar Chart', 'bar_chart'], ['Stacked Bar Chart', 'stacked_bar_chart']]
            chart_type_options_bar = dmc.RadioGroup(
                children=[dmc.Radio(l, value=v) for l, v in chart_types],
                value='bar_chart',
                id="sum_chart_type_options_bar",
                label="Chart Type",
                size="xs",
                mt=5,
                offset=4
            )
            
            # Get the selected chart type
            chart_type = chart_type_options_bar.value
            
            bar_chart_data, unique_turunan_var, value_type = data_processing.get_bar_chart_data(df, year, 'variable')

            value_types = [['Variable', 'variable']]
            if not (len(unique_turunan_var) == 1 and unique_turunan_var[0] == 'Tidak Ada'):
                value_types.append(['Turunan Variabel', 'turunan variable'])  # Ensure name matches the DataFrame

            value_type_options_bar = dmc.RadioGroup(
                children=[dmc.Radio(l, value=v) for l, v in value_types],
                value='variable',
                id="sum_value_type_options_bar",
                label="Value Type",
                size="xs",
                mt=5,
                offset=4
            )

            options_row = dmc.Group(
                children=[chart_type_options_bar, value_type_options_bar],
                spacing=15,
                align='center',
                position='left'
            )

            if chart_type == 'bar_chart':
                bar_chart_fig = plotly_visual.get_bar_chart_figure(bar_chart_data, year, value_type)

                bar_chart_graph = dcc.Graph(
                    figure=bar_chart_fig,
                    config={'displaylogo': False, 'modeBarButtonsToRemove': ['lasso2d', 'pan']},
                    id='sum_bar_chart_fig',
                    className='bar_chart_graph',
                    style=dict(width='', height='450px')  # Fixed height for single chart
                )

            else:  # Stacked Bar Chart
                if value_type == 'variable':
                    stacked_bar_fig = plotly_visual.get_stacked_bar_chart_figure(data_processing.get_filter_df(df), year, path=['variable', 'turunan variable'])
                else:
                    stacked_bar_fig = plotly_visual.get_stacked_bar_chart_figure(data_processing.get_filter_df(df), year, path=['turunan variable', 'variable'])

                bar_chart_graph = dcc.Graph(
                    figure=stacked_bar_fig,
                    config={'displaylogo': False, 'modeBarButtonsToRemove': ['lasso2d', 'pan']},
                    id='sum_bar_chart_fig',
                    className='stacked_bar_chart_graph',
                    style=dict(width='', height='450px')  # Fixed height for single chart
                )

        # bar_chart_graph = dbc.Spinner([bar_chart_graph], size="lg", color="primary", type="border", fullscreen=False)


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
                options_row if options_row else dmc.Space(),  # Ensure options_row is not None
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

    else:
        rotated_bar_fig = plotly_visual.get_rotated_bar_chart(data_processing.get_filter_df(df), year)

        bar_chart_graph = dcc.Graph(
            figure=rotated_bar_fig,
            config={'displaylogo': False, 'modeBarButtonsToRemove': ['lasso2d', 'pan']},
            id='sum_bar_chart_fig',
            className='bar_chart_graph',
            style=dict(width='', height='500px')
        )

        # bar_chart_graph = dbc.Spinner([bar_chart_graph], size="lg", color="primary", type="border", fullscreen=False)

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

def get_heatmap_layout(unit,selected_value,df, year, vertical_id, turunan_id):
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
        # option_turunan_variable = dmc.Select(
        #     style=dict(maxWidth='40%', display='none', height='49.8px'),
        # )
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

def sum_analysis_layout(unit, selected_value, df, year, vertical_id, turunan_id):
    if unit == "Tidak Ada Satuan":
        units=""
    else:
        units="("+unit+")"
    years = df.columns[4:].tolist()
    years_count = len(years)
    print(year)
    layout_item =[]

    if vertical_id != 1:
        if turunan_id == 1 and 'Jumlah' not in df['turunan variable'].unique():
            df= data_processing.preprocess_dataframe(df)
        pie_chart_col = get_pie_chart_col(units,selected_value,df, year, turunan_id)
        layout_item.append(pie_chart_col)
        heatmap_layout = get_heatmap_layout(units,selected_value,df,year,vertical_id, turunan_id)
        layout_item.append(heatmap_layout)
        bar_chart_layout = get_bar_chart_col(units,selected_value,df,year, turunan_id)
        layout_item.append(bar_chart_layout)
        if years_count>1:
            df = df[~df['variable'].str.contains('Riau|Provinsi Riau|Jumlah|Jumlah bukan makanan|Jumlah Makanan|PDRB', case=False)]
            time_series_chart_layout = get_time_series_layout(units, selected_value,df)
            layout_item.append(time_series_chart_layout)
        
        
    else:
        
        if years_count>1:
            time_series_chart_layout = get_time_series_layout(units,selected_value,df)
        layout_item.append(time_series_chart_layout)


    stats_cols = get_summary_sum(unit, df, year,vertical_id, turunan_id)

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
         dmc.Grid(layout_item, gutter=12, align="center",
        justify="space-around",style=dict(paddingLeft='1.3rem', paddingRight='1.3rem')),
         dmc.Space(h=20)],
         
    )
    
    return layout


