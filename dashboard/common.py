import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify
from dashboard import constants

def header_with_icon_div(icon_name, header_text, icon_color, icon_size, header_size):
    icon = DashIconify(icon=icon_name, color=icon_color, inline=True,
                       style=dict(fontSize=icon_size, verticalAlign='center'))

    header = html.Div(children=header_text,
                      className="content-with-icon-text",
                      style=dict(fontWeight=550,
                                 color='#272727', fontSize="1.3rem"))

    final_div = dmc.Group(children=[icon, header],
                          align='center',
                          spacing=8
                          )

    return final_div

def content_with_icon_div(icon_name, icon_bg_color, title_text, content_data, desc_data, id_value,  div_style=None):
    if id_value == "total":
        question_text="Nilai total merepresentasikan penjumlahan seluruh variabel dalam dataset."
    elif id_value == "max":
        question_text="Nilai max menunjukkan nilai terbesar dari semua variabel dalam dataset."
    elif id_value == "min":
        question_text="Nilai min menunjukkan nilai terkecil dari semua variabel dalam dataset."
    elif id_value == "growth":
        question_text="Nilai growth menunjukkan perubahan total dari waktu ke waktu."
    elif id_value == "top_growth":
        question_text="Nilai top growth menunjukkan variabel yang mengalami pertumbuhan terbesar dibandingkan dengan variabel lain dalam dataset."
    elif id_value == "average":
        question_text="menunjukkan nilai rata-rata dari variabel dalam dataset"
    else:
        question_text=""
    # Ikon utama
    icon = dmc.ThemeIcon(
        size="4x",
        color=icon_bg_color,
        variant="filled",
        style=dict(marginTop='', padding='10px'),
        children=DashIconify(
            icon=icon_name,
            inline=True,
            style=dict(fontSize='3rem')
        )
    )

    # Judul
    title = html.Div(
        children=title_text,
        style=dict(
            display='inline-block',
            color='#343434',
            textAlign="left",
            fontWeight=600,
            fontSize='0.75rem',
            paddingLeft="0.6rem",
        ),
    )

    # Data konten
    data = html.Div(children=content_data,
                    style=dict(
                        color='black',
                        display="inline-block",
                        paddingLeft="0.7rem",
                        fontWeight=500,
                        fontSize='1.2rem',
                    ),
                    className="content-with-icon-text",
                    id=id_value)

    # Deskripsi
    desc = html.Div(
        children=desc_data,
        style=dict(
            display='inline-block',
            color='#343434',
            textAlign="left",
            fontWeight=600,
            fontSize='0.75rem',
            paddingLeft="0.6rem",
        ),
        id=id_value + " desc"
    )

    # Ikon tanda tanya kecil
    question_icon = dmc.ActionIcon(
        DashIconify(icon="bi:question", color="#272727", inline=True,
                    style=dict(fontSize='1rem')),
        id=id_value + '-question-icon',
        variant='transparent'
    )

    # Modal untuk pop-up teks
    modal = dmc.Modal(
        title="Tentang "+title_text,
        id=id_value + '-info-modal',
        children=html.P(question_text),
        size='lg',
        opened=False
    )

    # Konten div dengan ikon dan teks
    content_div = dmc.Stack(children=[title, data, desc],
                            spacing=0,
                            style=dict(width=''))
    

    icontent_div = dmc.Grid(children=[icon, content_div],
                         align="flex-start",
                         justify="flex-start",
                         gutter="xl",
                         style=dict(padding='0.5rem')
                         )
    
    final_div = dmc.Group(children=[icontent_div, question_icon, modal],
                          position="apart",
                          align="start",
                          style=dict(padding='0.5rem'))


    return final_div

