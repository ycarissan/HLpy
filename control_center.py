from dessin_molecule import DessinMolecule
from chem_molecule import Molecule
from params import TYPE_ATOME
import numpy as np

class Control_Center:
    def __init__(self, canvas_molecule):
        self.molecule = Molecule()
        self.canvas_molecule = canvas_molecule
        self.dessin_molecule = DessinMolecule(self.canvas_molecule)
        self.correspondance = {"atome_dessin":[], "liaison_dessin":[]}

    def add_atom(self, x, y, type):
        atome = self.molecule.add_atom(type)
        dessin_atome = self.dessin_molecule.add_dessin_atome(x, y, type)
        self.correspondance["atome_dessin"].append((atome, dessin_atome))
        if type == "CARBONEsp2":
            for i in range(3):
                xH = x + 50*np.cos(2*np.pi/3*(i+1))
                yH = y + 50*np.sin(2*np.pi/3*(i+1))
                _ , dessin_hydrogene = self.add_atom(xH, yH, TYPE_ATOME.HYDROGENE)
                self.add_bond(dessin_atome, dessin_hydrogene)
        return atome, dessin_atome
    
    def remove_atom(self, dessin_atome):
        self.dessin_molecule.remove_dessin_atome(dessin_atome)
        atome = self.get_atome_from_dessin(dessin_atome)
        self.molecule.remove_atom(atome)
        self.correspondance["atome_dessin"].remove((atome, dessin_atome))

    def add_bond(self, dessin_atome1, dessin_atome2):
        atome1 = self.get_atome_from_dessin(dessin_atome1)
        atome2 = self.get_atome_from_dessin(dessin_atome2)
        dessin_liaison = self.dessin_molecule.add_bond(dessin_atome1, dessin_atome2)
        liaison = self.molecule.add_bond(atome1, atome2)
        self.correspondance["liaison_dessin"].append((liaison, dessin_liaison))

    def remove_bond(self, dessin_liaison):
        liaison = self.get_liaison_from_dessin(dessin_liaison)
        self.molecule.remove_bond(liaison)
        self.dessin_molecule.remove_liaison(dessin_liaison)

    def get_dessinAtom_at_position(self, x, y):
        return self.dessin_molecule.get_dessinAtom_at_position(x, y)
    
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
    
    def get_liaison_from_dessin(self, dessin_liaison):
        for liaison, dessin in self.correspondance["liaison_dessin"]:
            if dessin == dessin_liaison:
                return liaison
        return None
    
    def get_dessin_from_liaison(self, liaison):
        for liaison, dessin in self.correspondance["liaison_dessin"]:
            if liaison == liaison:
                return dessin
        return None