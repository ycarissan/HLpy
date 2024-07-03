from chem_atome import Atome

class Liaison:
    """
    Classe représentant une liaison.

    """

    def __init__(self, atome1: Atome, atome2: Atome):
        """
        Initialise un objet Liaison.

        Args:
            canvas (tkinter.Canvas): Le canvas sur lequel dessiner l'atome.
            atome1 (Atome): L'atome 1.
            atome2 (Atome): L'atome 2.
        """
        self.atome1 = atome1
        self.atome2 = atome2
    
    def get_other_atom(self, atom: Atome):
        """
        Récupère l'atome voisin de l'atome donné.

        Args:
            atom (Atome): L'atome donné.

        Returns:
            Atome: L'atome voisin.
        """
        if atom == self.atome1:
            return self.atome2
        elif atom == self.atome2:
            return self.atome1
        else:
            return None
