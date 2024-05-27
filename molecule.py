from atome import Atome
from liaison import Liaison

class Molecule:
    def __init__(self):
        self.atomes = []
        self.liaisons = []

    def add_atom(self, type):
        atome = Atome(type)
        self.atomes.append(atome)
        return atome
    
    def add_liaison(self, atom1, atom2):
        liaison = Liaison(atom1, atom2)
        self.liaisons.append(liaison)
        return liaison

