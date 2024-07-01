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
    
    def get_neighbours(self, atom):
        neighbours = []
        for liaison in self.liaisons:
            if atom in liaison.atomes:
                neighbours.append(liaison.get_other_atom(atom))
        return neighbours
    
    def get_huckel_neighbours(self, atom):
        huckel_neighbours = []
        for liaison in self.liaisons:
            if atom in liaison.atomes:
                other_atom = liaison.get_other_atom(atom)
                if other_atom.type != "hydrogen":
                    huckel_neighbours.append(other_atom)
        return huckel_neighbours
    
    def get_number_of_bonds(self, atom):
        return len(self.get_neighbours(atom))
    
    def get_number_of_huckel_bonds(self, atom):
        return len(self.get_huckel_neighbours(atom))
    
    def generate_huckel_connectivity_matrix(self):
        matrix = []
        for i in range(len(self.atomes)):
            row = []
            for j in range(len(self.atomes)):
                if self.atomes[j] in self.get_huckel_neighbours(self.atomes[i]):
                    row.append(1)
                else:
                    row.append(0)
            matrix.append(row)
        return matrix

