class Liaison:
    """
    Classe représentant une liaison.

    """

    def __init__(self, atome1, atome2):
        """
        Initialise un objet Liaison.

        Args:
            canvas (tkinter.Canvas): Le canvas sur lequel dessiner l'atome.
            atome1 (Atome): L'atome 1.
            atome2 (Atome): L'atome 2.
        """
        self.atome1 = atome1
        self.atome2 = atome2
