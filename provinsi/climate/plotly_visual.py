import dash_mantine_components as dmc
import plotly.graph_objects as go
import json
import pandas as pd
import plotly.express as px
from dashboard import constants, common


colors = [
    '#9C2424', '#0C9494', '#EC9C05', '#EAD4A4', '#C34F04', '#94D4BC',
    '#E49C1C', '#046474', '#0C7C84', '#8CDCD4', '#AC250B', '#01012C',
    '#123456', '#654321', '#ABCDEF', '#FEDCBA', '#FF5733', '#33FF57',
    '#3357FF', '#FF33A1', '#A133FF', '#33FFA1', '#A1FF33', '#FF7F50'
]

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
            color_continuous_scale="rdbu",
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
            x=df_filled["variable"].tolist(),
            y=df_filled["turunan variable"].tolist(),
            colorscale='rdbu',
            hoverongaps=False
        ))
        
        fig_heatmap.update_layout(
            xaxis_title='Turunan Variable',
            yaxis_title='Variable',
            xaxis=dict(side='bottom'),
            yaxis=dict(autorange='reversed'),
            margin=dict(l=50, r=50, t=50, b=50),
        )
        
        return fig_heatmap

    except Exception as e:
        return dmc.Alert(f"An error occurred: {str(e)}", color="red", title="Error")
      



def get_range_plot_figure(df, year):
    variables = df['variable'].unique().tolist()
    min_values = df[df['turunan variable'] == 'Minimum'][year].tolist()
    avg_values = df[df['turunan variable'] == 'Rata-Rata'][year].tolist()
    max_values = df[df['turunan variable'] == 'Maksimum'][year].tolist()

    fig = go.Figure()

    
    fig.add_trace(go.Scatter(
        x=variables,
        y=min_values,
        fill=None,
        mode='lines',
        line_color='lightgrey',
        showlegend=False
    ))

    fig.add_trace(go.Scatter(
        x=variables,
        y=max_values,
        fill='tonexty',  
        mode='lines',
        line_color='lightgrey',
        showlegend=False
    ))

    
    fig.add_trace(go.Scatter(
        x=variables,
        y=avg_values,
        mode='lines+markers',
        name='Average',
        line=dict(color=colors[0]),
        marker=dict(color=colors[0])
    ))

    fig.update_layout(
        xaxis_title='Month',
        yaxis_title='Value',
        hovermode='x unified'
    )

    return fig


def get_time_series_figure(traces):
    layout = {
        'xaxis': {'title': 'Value'},
        'yaxis': {'title': 'Month'},
        'hovermode': 'closest'
    }
    fig = go.Figure(data=traces, layout=layout)

    for i, trace in enumerate(fig.data):
        trace.marker.color = colors[i % len(colors)]

    return fig