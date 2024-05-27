import numpy as np

from molecule import Molecule
from atome import Atome
from liaison import Liaison
from params import params

class DessinMolecule:
    """
    Classe représentant une molécule.

    Attributs:
        canvas (tkinter.Canvas): Le canvas sur lequel dessiner la molécule.
        atomes (list): La liste des atomes de la molécule.
    """

    def __init__(self, canvas):
        """
        Initialise un objet DessinMolecule.

        Args:
            canvas (tkinter.Canvas): Le canvas sur lequel dessiner la molécule.
        """
        self.canvas = canvas
        self.molecule = Molecule()

    def add_carbon_atom(self, x, y):
        """
        Ajoute un atome de carbone à la molécule, avec ses atomes d'hydrogène liés.

        Args:
            x (int): La coordonnée x du centre de l'atome de carbone.
            y (int): La coordonnée y du centre de l'atome de carbone.
        """
        carbon = Atome(self.canvas, x, y, 'carbon')
        self.molecule.atomes.append(carbon)
        hydrogens = self.draw_hydrogen_atoms(x, y, carbon)
        self.molecule.atomes.extend(hydrogens)
        return carbon

    def draw_hydrogen_atoms(self, x, y, carbon):
        """
        Dessine les atomes d'hydrogène liés à un atome de carbone.

        Args:
            x (int): La coordonnée x du centre de l'atome de carbone.
            y (int): La coordonnée y du centre de l'atome de carbone.
            carbon (Atome): L'objet Atome représentant l'atome de carbone.

        Returns:
            list: La liste des objets Atome représentant les atomes d'hydrogène dessinés.
        """
        hydrogen_params = params['hydrogen']
        bond_length = params['carbon']['radius'] + hydrogen_params['radius'] + params['bond_width']
        hydrogens = []
        for angle in [0, 120, 240]:
            x_h = x + bond_length * np.cos(np.radians(angle))
            y_h = y + bond_length * np.sin(np.radians(angle))
            hydrogen = Atome(self.canvas, x_h, y_h, 'hydrogen')
            self.canvas.create_line(x, y, x_h, y_h, fill=params['bond_color'], width=params['bond_width'])
            hydrogens.append(hydrogen)
        return hydrogens
    
    def add_bond(self, atome1, atome2):
        liaison = Liaison(self.canvas, atome1, atome2)
        self.molecule.liaisons.append(liaison)
        return liaison

    def toggle_symbols(self):
        """
        Affiche ou masque les labels de tous les atomes de la molécule.
        """
        params['show_symbols'] = not params['show_symbols']
        for atom in self.molecule.atomes:
            atom.toggle_label()

    def get_atom_at_position(self, x, y):
        """
        Retourne l'atome situé aux coordonnées spécifiées, ou None si aucun atome n'est présent.

        Args:
            x (int): La coordonnée x de la position.
            y (int): La coordonnée y de la position.

        Returns:
            Atome ou None: L'objet Atome situé aux coordonnées spécifiées, ou None si aucun atome n'est présent.
        """
        for atom in self.molecule.atomes:
            dessin_atome = atom.dessin_atome
            if (dessin_atome.x - dessin_atome.params['radius'] <= x <= dessin_atome.x + dessin_atome.params['radius'] and
                dessin_atome.y - dessin_atome.params['radius'] <= y <= dessin_atome.y + dessin_atome.params['radius']):
                return atom
        return None

