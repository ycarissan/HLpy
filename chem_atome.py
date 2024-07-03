from params import *

class Atome:
    """
    Classe représentant un atome.

    Attributs:
        dessin_atome (DessinAtome): L'objet DessinAtome associé à l'atome.
    """

    def __init__(self, type_atome: TYPE_ATOME):
        """
        Initialise un objet Atome.

        Args:
            type_atome (str): Le type d'atome ('carbon' ou 'hydrogen').
        """
        self.type = type_atome

    def get_valence(self):
        """
        Renvoie la valence de l'atome.

        Returns:
            int: La valence de l'atome.
        """
        return params[self.type.value]['valence']
