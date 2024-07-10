import numpy as np

from dessin_atome import DessinAtome
from dessin_liaison import Dessin_liaison
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
        self.dessins = {'atomes': [], 'liaisons': []}

    def add_dessin_atome(self, x, y, type: TYPE_ATOME):
        dessinAtome = DessinAtome(self.canvas, x, y, type)
        self.dessins['atomes'].append(dessinAtome)
        return dessinAtome

    def remove_dessin_atome(self, dessin_atome):
        self.dessins['atomes'].remove(dessin_atome)
        self.redraw()

    def remove_dessin_liaison(self, dessin_liaison):
        self.dessins['liaisons'].remove(dessin_liaison)
        self.redraw()

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



