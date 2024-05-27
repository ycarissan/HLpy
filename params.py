# Dictionnaire des paramètres
from enum import Enum


class TYPE_ATOME(Enum):

    CARBONE = "CARBONEsp2"
    HYDROGENE = "HYDROGENE"


params = {
    'CARBONEsp2': {'radius': 20, 'color': 'gray', 'symbol': 'C'},
    'HYDROGENE': {'radius': 10, 'color': 'white', 'border_color': 'black', 'symbol': 'H'},
    'bond_color': 'red',
    'bond_width': 2,
    'show_symbols': True
}