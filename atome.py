from dessinAtome import DessinAtome

class Atome:
    """
    Classe représentant un atome.

    Attributs:
        dessin_atome (DessinAtome): L'objet DessinAtome associé à l'atome.
    """

    def __init__(self, canvas, x, y, atom_type):
        """
        Initialise un objet Atome.

        Args:
            canvas (tkinter.Canvas): Le canvas sur lequel dessiner l'atome.
            x (int): La coordonnée x du centre de l'atome.
            y (int): La coordonnée y du centre de l'atome.
            atom_type (str): Le type d'atome ('carbon' ou 'hydrogen').
        """
        self.dessin_atome = DessinAtome(canvas, x, y, atom_type)

    def toggle_label(self):
        """
        Affiche ou masque le label de l'atome.
        """
        self.dessin_atome.toggle_label()