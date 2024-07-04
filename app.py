from dashboard import init
from flask import Flask
import dash
import dash_bootstrap_components as dbc

server = Flask(__name__)

app = dash.Dash(
    name=__name__,
    suppress_callback_exceptions=True,
    assets_folder=f'assets',
    server=server,
    use_pages=True,
    pages_folder=f"pages",
    title='Badan Pusat Statistik Provinsi Riau',
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

init.init_app(app)

if __name__ == "__main__":
    app.run_server(debug=False, port=8570)