# Dictionnaire des paramètres
from enum import Enum


class TYPE_ATOME(Enum):

    CARBONE = "CARBONEsp2"
    HYDROGENE = "HYDROGENE"


params = {
    'CARBONEsp2': {'radius': 20, 'color': 'gray',  'symbol': 'C', 'valence': 3, 'border_color': 'black', 'isHuckel': True},
    'HYDROGENE':  {'radius': 10, 'color': 'white', 'symbol': 'H', 'valence': 1, 'border_color': 'black', 'isHuckel': False},
    'bond_color': 'red',
    'bond_width': 2,
    'show_symbols': True
}

def isHuckel(type):
    return params[type]['isHuckel']