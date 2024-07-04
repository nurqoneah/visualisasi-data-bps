import base64

import dash
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import html, dcc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from dash_iconify import DashIconify

from dashboard import constants
from provinsi.sum.callbacks import add_sum_callbacks
from provinsi.average.callbacks import add_average_callbacks
from provinsi.percent.callbacks import add_percent_callbacks
from provinsi.climate.callbacks import add_climate_callbacks
from provinsi.index.callbacks import add_index_callbacks
from provinsi.other.callbacks import add_other_callbacks
from provinsi.callbacks import add_province_callbacks
from kota.callbacks import add_city_callbacks


    


def get_links_div():
    tab1_icon = DashIconify(
        icon="wpf:statistics",
        color="",
        inline=True,
        className="tab_icon",
        style=dict(fontSize="1rem"),
    )

    tab1_text = html.Div(
        children="Analisis Provinsi",
        style=dict(paddingLeft="0.5rem", display="inline-block", color=""),
    )

    tab1_text_div = html.Div(
        children=[tab1_icon, tab1_text],
        style=dict(display="inline-block"),
        className="",
    )

    tab1 = dbc.NavItem(
        dbc.NavLink(
            tab1_text_div,
            active='exact',
            href='/AnalisisProvinsi',
            target="",
            id="mat_tab6",
            className="header-link",
            style=dict(fontSize="", textAlign=""),
        )
    )

    tab2_icon = DashIconify(
        icon="gis:world-map-alt",
        color="",
        inline=True,
        className="tab_icon",
        style=dict(fontSize="1rem"),
    )

    tab2_text = html.Div(
        children="Analisis Kota/Kabupaten",
        style=dict(paddingLeft="0.5rem", display="inline-block", color=""),
    )

    tab2_text_div = html.Div(
        children=[tab2_icon, tab2_text],
        style=dict(display="inline-block"),
        className="",
    )

    tab2 = dbc.NavItem(
        dbc.NavLink(
            tab2_text_div,
            active='exact',
            href='/AnalisisKota',
            target="",
            id="mat_tab7",
            className="header-link",
            style=dict(fontSize="", textAlign=""),
        )
    )

    tabs_links_div = html.Div(
        dbc.Nav(
            [tab1, tab2], pills=False, vertical=False
        ),
        style=dict(
            display="flex",
            alignItems="right",
            justifyContent="right",
            width="100%",
        ),
    )

    return tabs_links_div


header_text = html.Div('Badan Pusat Statistik', id='main_header_text', className='',
                       style=dict(color='white', paddingLeft='0.5rem',
                                  fontWeight='bold', fontSize='1.2rem', textAlign='left', display='inline-block'
                                  ))

header_text_col = dbc.Col([header_text],
                          xs=dict(size=7, offset=0), sm=dict(size=7, offset=0),
                          md=dict(size=6, offset=0), lg=dict(size=4, offset=0), xl=dict(size=4, offset=0)
                          )

encoded = base64.b64encode(open(constants.LOGO_DIRECTORY, 'rb').read())

logo_img = html.Img(src='data:image/jpg;base64,{}'.format(encoded.decode()), id='logo_img', height='50vh',
                    style=dict(padding='0.5rem', border=''))

logo_img = html.Div([logo_img], style=dict(display='inline-block'))

logo_img_col = dbc.Col([logo_img],
                       xs=dict(size=2, offset=0), sm=dict(size=2, offset=0),
                       md=dict(size=4, offset=0), lg=dict(size=1, offset=0), xl=dict(size=1, offset=0),
                       style=dict(border=''))

links_col = dbc.Col(
    dbc.Collapse(
        get_links_div(),
        id="navbar-collapse",
        is_open=False,
        navbar=True,
    ),
    xs=dict(size=3, offset=0),
    sm=dict(size=3, offset=0),
    md=dict(size=12, offset=0),
    lg=dict(size=6, offset=1),
    xl=dict(size=6, offset=1),
    style=dict(
        paddingLeft="1.5rem",
        paddingRight="1.5rem",
        paddingBottom="1rem",
    ),
)

navbar = dbc.Navbar(dbc.Container(
    [dmc.Grid([logo_img, header_text], align='center'),

     dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
     dbc.Collapse(
         get_links_div(),
         id="navbar-collapse",
         is_open=False,
         navbar=True,
     )
     ]),

    color=constants.MAIN_HEADER_BG,
    dark=True,
)

init_layout = html.Div([navbar, html.Br(),
                        dash.page_container,
                        html.Br(), html.Br(),
                        dcc.Location(id='url')
                        ]
                       , style=dict(backgroundColor=constants.APP_BG)
                       , className='main'
                       )


def add_init_callback(app: dash.Dash):
    

    @app.callback(
        Output("navbar-collapse", "is_open"),
        [Input("navbar-toggler", "n_clicks")],
        [State("navbar-collapse", "is_open")],
    )
    def toggle_navbar_collapse(n, is_open):
        if n:
            return not is_open
        return is_open

    @app.callback(
        Output("url", "pathname"),
        Input("url", "pathname")
    )
    def update_url(pathname):
        if pathname == '/':
            return '/AnalisisProvinsi'
        else:
            raise PreventUpdate


def init_app(app: dash.Dash):
    app.layout = init_layout
    add_init_callback(app)
    add_province_callbacks(app)
    add_sum_callbacks(app)
    add_average_callbacks(app)
    add_percent_callbacks(app)
    add_climate_callbacks(app)
    add_index_callbacks(app)
    add_other_callbacks(app)
    add_city_callbacks(app)
    

    


