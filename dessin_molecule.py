import numpy as np

from dessin_atome import DessinAtome
from dessin_liaison import Dessin_liaison
from chem_molecule import Molecule
from chem_atome import Atome
from chem_liaison import Liaison
from params import TYPE_ATOME, params
import pymunk

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
        dessinAtome = self.add_dessin_atome(x, y, type, atome)
        if atome.type.value == "CARBONEsp2":
            for i in range(3):
                hydrogen = self.molecule.add_atom(TYPE_ATOME.HYDROGENE)
                xH = x + 50*np.cos(2*np.pi/3*(i+1))
                yH = y + 50*np.sin(2*np.pi/3*(i+1))
                dessinHydrogen = self.add_dessin_atome(xH, yH, TYPE_ATOME.HYDROGENE, hydrogen)
                self.add_bond(self.get_dessin_from_atome(atome), dessinHydrogen)
        return dessinAtome

    def add_dessin_atome(self, x, y, type, atome):
        dessinAtome = DessinAtome(self.canvas, x, y, type)
        self.correspondance["atome_dessin"].append((atome, dessinAtome))
        self.dessins['atomes'].append(dessinAtome)
        return dessinAtome
    
    def remove_atom(self, dessin_atome):
        atome = self.get_atome_from_dessin(dessin_atome)
        self.molecule.remove_atom(atome)
        self.remove_dessin_atome(dessin_atome, atome)

    def remove_dessin_atome(self, dessin_atome, atome):
        self.dessins['atomes'].remove(dessin_atome)
        self.correspondance["atome_dessin"].remove((atome, dessin_atome))
        self.redraw()

    def remove_liaison(self, dessin_liaison):
        liaison = None
        for l, dessin in self.correspondance["liaison_dessin"]:
            if dessin == dessin_liaison:
                liaison = l
                break
        if liaison is None:
            return
        self.molecule.remove_bond(liaison)
        self.correspondance["liaison_dessin"].remove((liaison, dessin_liaison))
        self.dessins['liaisons'].remove(dessin_liaison)
        self.red

    def add_bond(self, dessin_atome1, dessin_atome2):
        atome1 = self.get_atome_from_dessin(dessin_atome1)
        atome2 = self.get_atome_from_dessin(dessin_atome2)

        if not(self.molecule.has_free_valency(atome1) and self.molecule.has_free_valency(atome2)):
            return None
        liaison = self.molecule.add_bond(atome1, atome2)
        self.replace_hydrogen_closest_to(atome1,atome2)
        self.replace_hydrogen_closest_to(atome2,atome1)
        #print(liaison, dessin_atome1, dessin_atome2)
        dessin_liaison = Dessin_liaison(self.canvas, dessin_atome1, dessin_atome2)
        self.correspondance["liaison_dessin"].append((liaison, dessin_liaison))
        self.dessins['liaisons'].append(dessin_liaison)
        return dessin_liaison
    
    def replace_hydrogen_closest_to(self, atome1: Atome, atome2: Atome):
        """
        Removes the hydrogen atom, which has a bond with atom1 and is closest to atom2
        """
        if atome1.type.value != "HYDROGENE" or atome2.type.value != "HYDROGENE":
            return
        #Look for the hydrogen atoms, which have a bond with atom1:
        hydrogens = self.molecule.get_non_huckel_neighbours(atome1)
        if len(hydrogens) == 0:
            raise Exception("No hydrogen atom found but expected: the test must have been done before!")
        #Look for the hydrogen atom, which is closest to atom2:
        closest_hydrogen = hydrogens[0]
        closest_distance = self.get_distance(atome2,closest_hydrogen)
        for hydrogen in hydrogens:
            distance = self.get_distance(atome2,closest_hydrogen)
            if distance < closest_distance:
                closest_hydrogen = hydrogen
                closest_distance = distance
        self.remove_atom(self.get_dessin_from_atome(closest_hydrogen))

    def get_distance(self, atome1, atome2):
        dessinAtome1 = self.get_dessin_from_atome(atome1)
        dessinAtome2 = self.get_dessin_from_atome(atome2)
        x1 = dessinAtome1.x
        y1 = dessinAtome1.y
        x2 = dessinAtome2.x
        y2 = dessinAtome2.y
        return np.sqrt((x1-x2)**2 + (y1-y2)**2)

    def toggle_symbols(self):
        """
        Affiche ou masque les labels de tous les atomes de la molécule.
        """
        params['show_symbols'] = not params['show_symbols']
        for dessin_atome in self.dessins['atomes']:
            dessin_atome.toggle_label()

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
    
    def redraw(self):
        """
        Redessine la molécule sur le canvas.
        """
        self.canvas.delete("all")
        for dessin_atome in self.dessins['atomes']:
            dessin_atome.draw()
        for dessin_liaison in self.dessins['liaisons']:
            dessin_liaison.draw()
    
    def optimize(self):
        """
        Optimize the molecule with the pymunk physics engine using springs between bound atoms.
        """
        space = pymunk.Space()
        space.gravity = (0, 0)  # No gravity

        for dessin_atome in self.dessins['atomes']:
            body = pymunk.Body()
            body.position = (dessin_atome.x, dessin_atome.y)
            shape = pymunk.Circle(body, dessin_atome.params['radius'])
            shape.mass = 10
            space.add(body, shape)
            dessin_atome.body = body
            dessin_atome.shape = shape
        
        for liaison, dessin_liaison in self.correspondance["liaison_dessin"]:
            atome1 = liaison.atome1
            atome2 = liaison.atome2
            dessinAtome1 = self.get_dessin_from_atome(atome1)
            dessinAtome2 = self.get_dessin_from_atome(atome2)
            body1 = dessinAtome1.body
            body2 = dessinAtome2.body
            spring = pymunk.DampedSpring(body1, body2, (0, 0), (0, 0), 100, 100, 0.5)
            space.add(spring)

        for i in range(10000):
            space.step(1/50)
            for dessin_atome in self.dessins['atomes']:
                dessin_atome.x, dessin_atome.y = dessin_atome.body.position
            self.redraw()
            self.canvas.update()



