from params import params

class Dessin_liaison:
    """
    Classe pour dessiner une liaison entre deux atomes sur un canvas.

    Attributs:
        canvas (tkinter.Canvas): Le canvas sur lequel dessiner l'atome.
        x1 (int): La coordonnée x du centre de l'atome1.
        y1 (int): La coordonnée y du centre de l'atome1.
        x2 (int): La coordonnée x du centre de l'atome2.
        y2 (int): La coordonnée y du centre de l'atome2.
        params (dict): Les paramètres de dessin de l'atome.
        line (int): L'identifiant de la ligne dessinée pour la liaison.
        label (int ou None): L'identifiant du label de la liaison (s'il existe).
    """

    def __init__(self, canvas, x1, y1, x2, y2):
        """
        Initialise un objet DessinLiaison.

        Args:
        canvas (tkinter.Canvas): Le canvas sur lequel dessiner l'atome.
        x1 (int): La coordonnée x du centre de l'atome1.
        y1 (int): La coordonnée y du centre de l'atome1.
        x2 (int): La coordonnée x du centre de l'atome2.
        y2 (int): La coordonnée y du centre de l'atome2.
        """
        self.canvas = canvas
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.color = params['bond_color']
        self.width = params['bond_width']
        self.line = self.draw_line()
        self.label = self.draw_label()

    def draw_line(self):
        """
        Dessine la ligne représentant la liaison sur le canvas.

        Returns:
            int: L'identifiant de la ligne dessinée.
        """
        x1 = self.x1
        y1 = self.y1
        x2 = self.x2
        y2 = self.y2
        return self.canvas.create_line(x1, y1, x2, y2, fill=self.color, width=self.width)

    def draw_label(self):
        """
        Dessine le label de l'atome sur le canvas (s'il doit être affiché).

        Returns:
            int ou None: L'identifiant du label dessiné, ou None si aucun label n'est dessiné.
        """
        if params['show_symbols']:
            return self.canvas.create_text((self.x1+self.x2)*0.5, (self.y1+self.y2)*0.5, text="Liaison")
        return None
