from dash import register_page

from provinsi.layout import province_analysis_layout

register_page(__name__, path="/AnalisisProvinsi", layout=province_analysis_layout())