from params import TYPE_ATOME, params

class DessinAtome:
    """
    Classe  pour dessiner un atome sur un canvas.

    Attributs:
        canvas (tkinter.Canvas): Le canvas sur lequel dessiner l'atome.
        x (int): La coordonnée x du centre de l'atome.
        y (int): La coordonnée y du centre de l'atome.
        atom_type (str): Le type d'atome ('carbon' ou 'hydrogen').
        params (dict): Les paramètres de dessin de l'atome.
        circle (int): L'identifiant du cercle dessiné pour l'atome.
        label (int ou None): L'identifiant du label de l'atome (s'il existe).
    """

    def __init__(self, canvas, x, y, atom_type: TYPE_ATOME):
        """
        Initialise un objet DessinAtome.

        Args:
            canvas (tkinter.Canvas): Le canvas sur lequel dessiner l'atome.
            x (int): La coordonnée x du centre de l'atome.
            y (int): La coordonnée y du centre de l'atome.
            atom_type (str): Le type d'atome ('carbon' ou 'hydrogen').
        """
        self.canvas = canvas
        self.x = x
        self.y = y
        self.atom_type = atom_type
        self.params = params[atom_type.value]
        self.circle = self.draw_circle()
        self.label = self.draw_label()

    def draw_circle(self):
        """
        Dessine le cercle représentant l'atome sur le canvas.

        Returns:
            int: L'identifiant du cercle dessiné.
        """
        x1 = self.x - self.params['radius']
        y1 = self.y - self.params['radius']
        x2 = self.x + self.params['radius']
        y2 = self.y + self.params['radius']
        return self.canvas.create_oval(x1, y1, x2, y2, fill=self.params['color'], outline=self.params.get('border_color', self.params['color']))

    def draw_label(self):
        """
        Dessine le label de l'atome sur le canvas (s'il doit être affiché).

        Returns:
            int ou None: L'identifiant du label dessiné, ou None si aucun label n'est dessiné.
        """
        if params['show_symbols']:
            return self.canvas.create_text(self.x, self.y, text=self.params['symbol'])
        return None

    def change_color(self, new_color):
        """
        Change la couleur de l'atome.

        Args:
            new_color (str): La nouvelle couleur de l'atome.
        """
        self.canvas.itemconfig(self.circle, fill=new_color)

    def toggle_label(self):
        """
        Affiche ou masque le label de l'atome.
        """
        if self.label:
            self.canvas.delete(self.label)
            self.label = None
        else:
            self.label = self.draw_label()

