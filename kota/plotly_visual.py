import plotly.graph_objects as go
import json
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
from provinsi.sum import data_processing

colors = [
    '#9C2424', '#0C9494', '#EC9C05', '#EAD4A4', '#C34F04', '#94D4BC',
    '#E49C1C', '#046474', '#0C7C84', '#8CDCD4', '#AC250B', '#01012C',
    '#123456', '#654321', '#ABCDEF', '#FEDCBA', '#FF5733', '#33FF57',
    '#3357FF', '#FF33A1', '#A133FF', '#33FFA1', '#A1FF33', '#FF7F50'
]



def get_heatmap_figure(df, year):
    try:
        df_filled = df.fillna(0)
        
        fig_heatmap = go.Figure(data=go.Heatmap(
            z=df_filled[year].values.tolist(),
            x=df_filled["turunan variable"].tolist(),
            y=df_filled["variable"].tolist(),
            colorscale='darkmint',
            hoverongaps=False
        ))
        
        fig_heatmap.update_layout(
            xaxis_title='Variable',
            yaxis_title='Turunan Variable',
            xaxis=dict(side='bottom'),
            yaxis=dict(autorange='reversed'),
            margin=dict(l=50, r=50, t=50, b=50),
        )
        
        return fig_heatmap

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def get_bar_chart_figure(df, year, chart_type):
    if chart_type == 'variable':
        labels = df['variable']
        values = df[year]
    else:
        labels = df['turunan variable']
        values = df[year]

    fig = go.Figure(data=[go.Bar(x=labels, y=values, marker_color=colors)])

    fig.update_layout(
        margin=dict(l=0, r=0, t=30, b=30),
        xaxis_title=chart_type.capitalize(),
        yaxis_title='Values',
    )
    
    return fig

def get_stacked_bar_chart_figure(df, year, path):
    df_filtered = df[['variable', 'turunan variable', year]]

    if path == ['variable', 'turunan variable']:
        fig = px.bar(df_filtered, x='variable', y=year, color='turunan variable', color_discrete_sequence=colors)
    else:
        fig = px.bar(df_filtered, x='turunan variable', y=year, color='variable', color_discrete_sequence=colors)

    fig.update_layout(
        barmode='stack',
        margin=dict(l=0, r=0, t=30, b=30),
    )

    return fig

def get_rotated_bar_chart(df, year):
    variables = df['variable'].unique()
    turunan_variables = df['turunan variable'].unique()

    fig = go.Figure()

    for idx, turunan_variable in enumerate(turunan_variables):
        filtered_df = df[df['turunan variable'] == turunan_variable]
        values = filtered_df[year].tolist()

        fig.add_trace(go.Bar(
            x=variables,
            y=values,
            name=turunan_variable,
            marker_color=colors[idx % len(colors)]
        ))

    fig.update_layout(
        barmode='group',
        margin=dict(l=0, r=0, t=30, b=30),
        xaxis_title="Variable",
        yaxis_title="Value"
    )

    return fig

def get_time_series_figure(traces):
    layout = {
        'xaxis': {'title': 'Year'},
        'yaxis': {'title': 'Value'},
        'hovermode': 'closest'
    }
    fig = go.Figure(data=traces, layout=layout)

    for i, trace in enumerate(fig.data):
        trace.marker.color = colors[i % len(colors)]

    return fig
