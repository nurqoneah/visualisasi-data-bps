import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify
from dashboard import constants


# def spinner_with_text(text="Load Visualisasi", size="lg", color="primary", spinner_type="border"):
#         return html.Div(
#             [
#                 dbc.Spinner(size=size, color=color, type=spinner_type, spinner_style={'width': '5rem', 'height': '5rem'}),
#                 html.Div(text, style={'marginTop': '10px', 'fontSize': '16px', 'color': color})
#             ],
#             style={'textAlign': 'center', 'paddingTop': '20px'}
#         )




def header_with_icon_div(icon_name, header_text, icon_color, icon_size, header_size):
    icon = DashIconify(icon=icon_name, color=icon_color, inline=True,
                       style=dict(fontSize=icon_size, verticalAlign='center'))

    header = html.Div(children=header_text,
                      style=dict(fontWeight='bold',
                                 color='#272727', fontSize=header_size, fontFamily='Circular Std',

                                 ))

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
                        fontFamily='Circular Std',
                        paddingLeft="0.7rem",
                        fontWeight=600,
                        fontSize='1.2rem',
                    ),
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

# def header_with_icon_div(icon_name, header_text, icon_color, icon_size, header_size, question_text="hehehehe"):
#     # Icon utama
#     icon = DashIconify(icon=icon_name, color=icon_color, inline=True,
#                        style=dict(fontSize=icon_size, verticalAlign='center'))

#     # Header teks
#     header = html.Div(children=header_text,
#                       style=dict(fontWeight='bold',
#                                  color='#272727', fontSize=header_size, fontFamily='Circular Std'))

#     # Ikon tanda tanya kecil
#     question_icon = dmc.ActionIcon(
#         DashIconify(icon="mdi:question-mark-circle", color="#272727", inline=True,
#                     style=dict(fontSize=icon_size * 0.6)),
#         id='question-icon',
#         variant='transparent'
#     )

#     # Modal untuk pop-up teks
#     modal = dmc.Modal(
#         title="Information",
#         id='info-modal',
#         children=html.P(question_text),
#         size='lg',
#         opened=False
#     )

#     # Grup untuk menyatukan ikon utama, header, dan ikon tanda tanya
#     final_div = dmc.Group(children=[icon, header, question_icon, modal],
#                           align='center',
#                           spacing=8,
#                           position="apart"
#                           )

#     return final_div

# def content_with_icon_div(icon_name, icon_bg_color, title_text, content_data, desc_data, id_value,div_style=None):
#     icon = dmc.ThemeIcon(
#         size="4x", 
#         color=icon_bg_color,
#         variant="filled",
#         style=dict(marginTop='', padding='10px'),
#         children=DashIconify(
#             icon=icon_name, 
#             inline=True,
#             style=dict(fontSize='3rem')
#         )
#     )

#     title = html.Div(
#         children=title_text,
#         style=dict(
#             display='inline-block',
#             color='#343434',
#             textAlign="left",
#             fontWeight=600,
#             fontSize='0.75rem',
#             paddingLeft="0.6rem",
#         ),
#     )

#     data = html.Div(children=content_data,
#                     style=dict(
#                         color='black',
#                         display="inline-block",
#                         fontFamily='Circular Std',
#                         paddingLeft="0.7rem",
#                         fontWeight=600,
#                         fontSize='1.2rem',
#                     ),
#                     id=id_value)
    
#     desc = html.Div(
#         children=desc_data,
#         style=dict(
#             display='inline-block',
#             color=constants.MAIN_HEADER_BG,
#             textAlign="left",
#             fontWeight=600,
#             fontSize='0.75rem',
#             paddingLeft="0.6rem",
#         ),
#         id=id_value+" desc"
#     )
#     content_div = dmc.Stack(children=[title, data, desc],
#                             spacing=0,
#                             style=dict(width='')
#                             )

#     final_div = dmc.Grid(children=[icon, content_div],
#                          align="flex-start",
#                          justify="flex-start",
#                          gutter="xl",
#                          style=dict(padding='0.5rem')
#                          )

#     return final_div

