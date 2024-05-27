from dessinLiaison import Dessin_liaison

class Liaison:
    """
    Classe représentant une liaison.

    Attributs:
        dessin_liaison (DessinLiaison): L'objet DessinLiaison associé à la liaison.
    """

    def __init__(self, canvas, atome1, atome2):
        """
        Initialise un objet Liaison.

        Args:
            canvas (tkinter.Canvas): Le canvas sur lequel dessiner l'atome.
            atome1 (Atome): L'atome 1.
            atome2 (Atome): L'atome 2.
        """
        x1 = atome1.dessin_atome.x
        y1 = atome1.dessin_atome.y
        x2 = atome2.dessin_atome.x
        y2 = atome2.dessin_atome.y
        self.dessin_liaison = Dessin_liaison(canvas, x1, y1, x2, y2)