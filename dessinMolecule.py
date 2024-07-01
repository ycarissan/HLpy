import numpy as np

from dessinAtome import DessinAtome
from dessinLiaison import Dessin_liaison
from molecule import Molecule
from atome import Atome
from liaison import Liaison
from params import TYPE_ATOME, params

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
        self.dessins = {'atomes': [], 'liaisons': []}
        self.correspondance = {"atome_dessin":[], "liaison_dessin":[]}

    def add_atom(self, x, y, type: TYPE_ATOME):
        """
        Ajoute un atome de carbone à la molécule, avec ses atomes d'hydrogène liés.

        Args:
            x (int): La coordonnée x du centre de l'atome de carbone.
            y (int): La coordonnée y du centre de l'atome de carbone.
        """
        atome = self.molecule.add_atom(type)
        dessinAtome = DessinAtome(self.canvas, x, y, type)
        self.correspondance["atome_dessin"].append((atome, dessinAtome))
        self.dessins['atomes'].append(dessinAtome)
#        hydrogens = self.draw_hydrogen_atoms(x, y, atom)
#        self.molecule.atomes.extend(hydrogens)
        return dessinAtome

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
    
    def add_bond(self, dessinAtome1, dessinAtome2):
        atome1 = self.get_atome_from_dessin(dessinAtome1)
        atome2 = self.get_atome_from_dessin(dessinAtome2)
        liaison = self.molecule.add_liaison(atome1, atome2)
        print(liaison, dessinAtome1, dessinAtome2)
        dessinLiaison = Dessin_liaison(self.canvas, dessinAtome1.x, dessinAtome1.y, dessinAtome2.x, dessinAtome2.y)
        self.correspondance["liaison_dessin"].append((liaison, dessinLiaison))
        self.dessins['liaisons'].append(dessinLiaison)
        return dessinLiaison

    def toggle_symbols(self):
        """
        Affiche ou masque les labels de tous les atomes de la molécule.
        """
        params['show_symbols'] = not params['show_symbols']
        for atom in self.molecule.atomes:
            atom.toggle_label()

    def get_dessinAtom_at_position(self, x, y) -> DessinAtome:
        """
        Retourne le dessin de l'atome situé aux coordonnées spécifiées, ou None si aucun atome n'est présent.

        Args:
            x (int): La coordonnée x de la position.
            y (int): La coordonnée y de la position.

        Returns:
            Atome ou None: L'objet Atome situé aux coordonnées spécifiées, ou None si aucun atome n'est présent.
        """
        for dessin_atome in self.dessins['atomes']:
            if (dessin_atome.x - dessin_atome.params['radius'] <= x <= dessin_atome.x + dessin_atome.params['radius'] and
                dessin_atome.y - dessin_atome.params['radius'] <= y <= dessin_atome.y + dessin_atome.params['radius']):
                return dessin_atome
        return None
    
    def get_atome_from_dessin(self, dessin_atome):
        for atome, dessin in self.correspondance["atome_dessin"]:
            if dessin == dessin_atome:
                return atome
        return None

    def get_dessin_from_atome(self, at):
        for atome, dessin in self.correspondance["atome_dessin"]:
            if at == atome:
                return dessin
        return None

