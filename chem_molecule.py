from chem_atome import Atome
from chem_liaison import Liaison
from chem_wavefunction import Wavefunction
from params import TYPE_ATOME

class Molecule:
    def __init__(self):
        self.atomes = []
        self.liaisons = []
        self.wavefunction = Wavefunction("molecule", self.generate_huckel_connectivity_matrix(), [0])

    def update_wavefunction(self):
        self.wavefunction.set_matrix(self.generate_huckel_connectivity_matrix())
        return
    
    def add_atom(self, type: TYPE_ATOME):
        atome = Atome(type)
        self.atomes.append(atome)
        self.update_wavefunction()
        return atome
    
    def add_liaison(self, atom1: Atome, atom2: Atome):
        liaison = Liaison(atom1, atom2)
        self.liaisons.append(liaison)
        self.update_wavefunction()
        return liaison
    
    def get_neighbours(self, atom: Atome):
        neighbours = []
        for liaison in self.liaisons:
            if atom == liaison.atome1:
                neighbours.append(liaison.atome2)
            elif atom == liaison.atome2:
                neighbours.append(liaison.atome1)
        return neighbours
    
    def get_huckel_neighbours(self, atom: Atome):
        huckel_neighbours = []
        for liaison in self.liaisons:
            if atom in (liaison.atome1, liaison.atome2):
                other_atom = liaison.get_other_atom(atom)
                if other_atom.type != "hydrogen":
                    huckel_neighbours.append(other_atom)
        return huckel_neighbours
    
    def get_number_of_bonds(self, atom: Atome):
        return len(self.get_neighbours(atom))
    
    def get_number_of_huckel_bonds(self, atom: Atome):
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
    
    def has_free_valency(self, atom: Atome):
        return self.get_number_of_bonds(atom) < atom.get_valence()

