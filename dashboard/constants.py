import os
import stadata
import pandas as pd

TOKEN='0b5b67b65383eb275017dd5a676a0a38'

# TOKEN = "[YOUR_APP_ID]"

data_kota = {
        "id_var_kota": [1471,1401, 1402, 1403, 1404, 1405, 1406, 1407, 1408, 1409, 1410,  1473],
        "variable_kota": [
            "Pekanbaru","Kuantan Singingi", "Indragiri Hulu", "Indragiri Hilir", "Pelalawan", "Siak", "Kampar",
            "Rokan Hulu", "Bengkalis", "Rokan Hilir", "Kepulauan Meranti",  "Dumai"
        ],
    }

DATA_KOTA_DF = pd.DataFrame(data_kota)

APP_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
LOGO_DIRECTORY = os.path.join(APP_DIRECTORY, 'bps.png')
CSV_FILE_DIRECTORY = os.path.join(APP_DIRECTORY, 'note_1.csv')
CSV_FILE_DIRECTORY_CITY= os.path.join(APP_DIRECTORY, 'kota-kab-2.csv')

MAIN_HEADER_BG = '#01012c'
DASHBOARD_MAIN_COLOR1 = '#045C74'
DASHBOARD_MAIN_COLOR3 = '#EAD4A4'
DASHBOARD_MAIN_COLOR2 = '#C34F04'
DASHBOARD_MAIN_COLOR4 = '#0C9494'
DASHBOARD_MAIN_COLOR5 = '#94D4BC'

APP_BG = '#EBECF0'
