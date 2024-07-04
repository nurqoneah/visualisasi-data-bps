from dash import register_page

from kota.layout import city_analysis_layout

register_page(__name__, path="/AnalisisKota", layout=city_analysis_layout())