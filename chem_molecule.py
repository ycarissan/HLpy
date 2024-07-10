from chem_atome import Atome
from chem_liaison import Liaison
from chem_wavefunction import Wavefunction
from params import params,TYPE_ATOME

class Molecule:
    """
    Represents a molecule.

    Attributes:
    - atomes (list): A list of atoms in the molecule.
    - liaisons (list): A list of bonds between atoms in the molecule.
    - wavefunction (Wavefunction): The wavefunction associated with the molecule.

    Methods:
    - update_wavefunction(): Updates the wavefunction of the molecule.
    - add_atom(type: TYPE_ATOME): Adds an atom of the specified type to the molecule.
    - remove_atom(atom: Atome): Removes the specified atom from the molecule.
    - remove_bond(liaison: Liaison): Removes a bond from the molecule.
    - add_bond(atom1: Atome, atom2: Atome): Adds a bond between two atoms in the molecule.
    - get_neighbours(atom: Atome): Returns a list of neighbouring atoms for the given atom.
    - get_huckel_neighbours(atom: Atome): Returns a list of Huckel neighbours for the given atom.
    - get_number_of_bonds(atom: Atome): Returns the number of bonds for the given atom.
    - get_number_of_huckel_bonds(atom: Atome): Returns the number of Huckel bonds for the given atom.
    - generate_huckel_connectivity_matrix(): Generates the Huckel connectivity matrix for the molecule.
    - has_free_valency(atom: Atome): Checks if the given atom has free valency.

    """

    def __init__(self):
        self.atomes = []
        self.liaisons = []
        self.wavefunction = Wavefunction("molecule", self.generate_huckel_connectivity_matrix(), [0])

    def update_wavefunction(self):
        self.wavefunction.set_matrix(self.generate_huckel_connectivity_matrix())
        return
    
    def add_atom(self, type: TYPE_ATOME):
        """
        Adds an atom of the specified type to the molecule.

        Parameters:
        - type (TYPE_ATOME): The type of atom to add.

        Returns:
        - atome (Atome): The newly added atom.

        """
        atome = Atome(type)
        self.atomes.append(atome)
        if params[type.value]['isHuckel']:
            self.update_wavefunction()
        return atome
    
    def remove_atom(self, atom: Atome):
        """
        Removes the specified atom from the molecule.

        Args:
            atom (Atome): The atom to be removed.

        Returns:
            None
        """
        self.atomes.remove(atom)
        for liaison in self.liaisons:
            if atom in (liaison.atome1, liaison.atome2):
                other_atom = liaison.get_other_atom(atom)
                if other_atom.type == TYPE_ATOME.HYDROGENE:
                    self.atomes.remove(other_atom)
                self.liaisons.remove(liaison)
        self.update_wavefunction()
        return
    
    def remove_bond(self, liaison: Liaison):
        """
        Removes a bond from the molecule.

        Args:
            liaison (Liaison): The bond to be removed.

        Returns:
            None
        """
        self.liaisons.remove(liaison)
        self.update_wavefunction()
        return
    
    def add_bond(self, atom1: Atome, atom2: Atome):
        """
        Adds a bond between two atoms in the molecule.

        Args:
            atom1 (Atome): The first atom.
            atom2 (Atome): The second atom.

        Returns:
            liaison (Liaison): The newly added bond.
        """
        liaison = Liaison(atom1, atom2)
        self.liaisons.append(liaison)
        self.update_wavefunction()
        return liaison
    
    def get_neighbours(self, atom: Atome):
        """
        Returns a list of neighbouring atoms for the given atom.

        Parameters:
        - atom (Atome): The atom for which to find neighbours.

        Returns:
        - list: A list of neighbouring atoms.
        """
        neighbours = []
        for liaison in self.liaisons:
            if atom == liaison.atome1:
                neighbours.append(liaison.atome2)
            elif atom == liaison.atome2:
                neighbours.append(liaison.atome1)
        return neighbours
    
    def get_huckel_neighbours(self, atom: Atome):
        """
        Returns a list of Huckel neighbours for the given atom.

        Parameters:
        - atom (Atome): The atom for which to find Huckel neighbours.

        Returns:
        - huckel_neighbours (list): A list of atoms that are Huckel neighbours of the given atom.
        """
        huckel_neighbours = []
        for liaison in self.liaisons:
            if atom in (liaison.atome1, liaison.atome2):
                other_atom = liaison.get_other_atom(atom)
                if params[other_atom.type.value]['isHuckel']:
                    huckel_neighbours.append(other_atom)
        return huckel_neighbours
    
    def get_non_huckel_neighbours(self, atom: Atome):
        """
        Returns a list of non-Huckel neighbours for the given atom.

        Parameters:
        - atom (Atome): The atom for which to find non-Huckel neighbours.

        Returns:
        - non_huckel_neighbours (list): A list of atoms that are not Huckel neighbours of the given atom.
        """
        non_huckel_neighbours = []
        for liaison in self.liaisons:
            if atom in (liaison.atome1, liaison.atome2):
                other_atom = liaison.get_other_atom(atom)
                if not params[other_atom.type.value]['isHuckel']:
                    non_huckel_neighbours.append(other_atom)
        return non_huckel_neighbours
    
    def get_number_of_bonds(self, atom: Atome):
        """
        Returns the number of bonds for the given atom.

        Parameters:
        - atom (Atome): The atom for which to count the bonds.

        Returns:
        - int: The number of bonds.
        """
        return len(self.get_neighbours(atom))
    
    def get_number_of_huckel_bonds(self, atom: Atome):
        """
        Returns the number of Huckel bonds for the given atom.

        Parameters:
        - atom (Atome): The atom for which to count the Huckel bonds.

        Returns:
        - int: The number of Huckel bonds.
        """
        return len(self.get_huckel_neighbours(atom))
    
    def generate_huckel_connectivity_matrix(self):
        """
        Generates the Huckel connectivity matrix for the molecule.

        Returns:
        - matrix (list): The Huckel connectivity matrix.
        """
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
        """
        Checks if the given atom has free valency.

        Parameters:
        - atom (Atome): The atom to check.

        Returns:
        - bool: True if the atom has free valency, False otherwise.
        """
        return self.get_number_of_huckel_bonds(atom) < atom.get_valence()

