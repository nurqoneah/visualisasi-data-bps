import dash_mantine_components as dmc
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

def get_pie_chart_figure(df, year):
    labels = df['variable']
    values = df[year]

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, marker=dict(colors=colors))])
    
    fig.update_layout(
        margin=dict(l=0, r=0, t=30, b=30)
    )
    
    return fig

def get_mul_pie_chart_figure(df, year):
    variables = df['variable'].unique()
    num_charts = len(variables)

    fig = make_subplots(rows=1, cols=num_charts, specs=[[{'type': 'domain'}]*num_charts])

    for idx, variable in enumerate(variables):
        
        filtered_df = df[df['variable'] ==variable]
        labels = filtered_df['turunan variable']
        values = filtered_df[year]

        fig.add_trace(go.Pie(labels=labels, values=values, marker=dict(colors=colors)), row=1, col=idx+1)

    fig.update_layout(
        annotations=[dict(text=variable, x=(idx+0.5)/num_charts, y=0.5, font_size=8, showarrow=False) for idx, variable in enumerate(variables)]
    )

    return fig


def get_sunburst_chart_figure(df, year):
    fig = px.sunburst(df, path=['variable', 'turunan variable'], values=year, color_discrete_sequence=colors)
    return fig

def get_heatmap_geos_figure(df, year):
    try:
        with open("./data/Indonesia_cities.geojson") as file_json:
            riau_geojson = json.load(file_json)

        riau_geojson["features"] = [f for f in riau_geojson["features"] if f["properties"]["NAME_1"] == "Riau"]

        all_cities = [f["properties"]["NAME_2"] for f in riau_geojson["features"]]
        df_all_cities = pd.DataFrame({"variable": all_cities})
        df_merged = pd.merge(df_all_cities, df, on="variable", how="left")
        
        fig_choropleth = px.choropleth(
            df_merged.fillna(0),
            geojson=riau_geojson,
            locations='variable',
            featureidkey="properties.NAME_2",  
            color=year,
            color_continuous_scale="darkmint",
            range_color=(df[year].min(), df[year].max()),
            labels={'color': 'Judul'},
        )

        fig_choropleth.update_geos(fitbounds="locations", visible=False)
        fig_choropleth.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        
        return fig_choropleth

    except Exception as e:
        return dmc.Alert(f"An error occurred: {str(e)}", color="red", title="Error")
        
        

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
        return dmc.Alert(f"An error occurred: {str(e)}", color="red", title="Error")


def get_stacked_bar_chart_figure(df, year, turunan_id):
    df_filtered = df[['variable', 'turunan variable', year]]
    if turunan_id == 1:
        fig = px.bar(df_filtered, y='variable', x=year, color='turunan variable', orientation='h', color_discrete_sequence=colors)
    else:
        fig = px.bar(df_filtered, y='turunan variable', x=year, color='variable', orientation='h', color_discrete_sequence=colors)
    fig.update_layout(
        barmode='stack',
        margin=dict(l=0, r=0, t=30, b=30),
    )

    return fig



def get_area_chart_figure(df):
    years = df.columns[4:].tolist()
   

    traces = []
    for i, (index, row) in enumerate(df.iterrows()):
        trace = go.Scatter(
            x=years,
            y=row[4:],
            mode='lines',
            name=row['variable'], 
            stackgroup='one',
            line=dict(color=colors[i]), 
            fill='tonexty'
        )
        traces.append(trace)

    layout = go.Layout(
        xaxis=dict(title='Year'),
        yaxis=dict(title='Value'),
        hovermode='closest',
        margin=dict(l=0, r=0, t=30, b=30)
    )

    
    fig = go.Figure(data=traces, layout=layout)

    return fig