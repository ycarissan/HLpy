import numpy as np
import xml.etree.ElementTree as ET

#class wavefunction
class Wavefunction:
    def __init__(self, name, matrix, occupation):
        self.name = name
        self.matrix = matrix
        self.occupation = occupation
        self.update()
    
    def huckel(self):
        # get eigenfunctions and eigenvalues from matrix using numpy
        eigenvalues, eigenfunctions = np.linalg.eigh(self.matrix)

        # order eigenvalues and eigenfunctions by descending eigenvalues
        idx = eigenvalues.argsort()[::-1]
        eigenvalues = eigenvalues[idx]
        eigenfunctions = eigenfunctions[:,idx]

        # compute Huckel energy
        huckel_energy = 0
        for i in range(len(self.occupation)):
            huckel_energy += self.occupation[i]*eigenvalues[i]
        return eigenvalues, eigenfunctions, huckel_energy
    
    def update(self):
        self.eigenvalues, self.eigenfunctions, self.huckel_energy = self.huckel()

    def get_name(self):
        return self.name
    
    def get_matrix(self):
        return self.matrix
    
    def get_occupation(self):
        return self.occupation
    
    def get_eigenvalues(self):
        return self.eigenvalues
    
    def get_eigenfunctions(self):
        return self.eigenfunctions
    
    def get_huckel_energy(self):
        return self.huckel_energy
    
    def set_name(self, name):
        self.name = name
    
    def set_occupation(self, occupation):
        self.occupation = occupation
        self.update()

    def get_eigenfunction(self, i):
        return self.eigenfunctions[:,i]

    def get_eigenvalue(self, i):
        return self.eigenvalues[i]
    
    def get_occupied_eigenfunctions(self):
        occupied_eigenfunctions = []
        for i in range(len(self.occupation)):
            if self.occupation[i] > 0:
                occupied_eigenfunctions.append(self.eigenfunctions[:,i])
        return occupied_eigenfunctions
    
    def get_overlap_matrix(self, that):
        occ_MO_this = self.get_occupied_eigenfunctions()
        occ_MO_that = that.get_occupied_eigenfunctions()
        overlap_matrix = np.zeros((len(occ_MO_this), len(occ_MO_that)))  # Define overlap_matrix
        for i in range(len(occ_MO_this)):
            MO_i = occ_MO_this[i]
            for j in range(len(occ_MO_that)):
                MO_j = occ_MO_that[j]
                overlap_matrix[i][j] = np.dot(MO_i, MO_j)
        return overlap_matrix

    def get_overlap_wf(self, that):
        overlap_matrix = self.get_overlap_matrix(that)
        print(overlap_matrix)
        overlap_wf = np.linalg.det(overlap_matrix)
        return overlap_wf
    
def read_wavefunctions_from_xml(file_path):
    """
    Read wavefunctions from an XML file.

    Args:
        file_path (str): The path to the XML file.

    Returns:
        list: A list of matrices extracted from the XML file.
    """
    wavefunctions = []
    tree = ET.parse(file_path)
    root = tree.getroot()
    for wavefunction in root.findall('wavefunction'):
        name = wavefunction.get('name')
        print("Reading wavefunction... {}".format(name))
        matrix = []
        for row in wavefunction.findall('row'):
            matrix.append([float(el) for el in row.text.split(' ')])
        occupation = [ int(i) for i in wavefunction.find('occupation').text.split(' ') ]
        wf = Wavefunction(name, np.array(matrix), occupation)
        wavefunctions.append(wf)
        print("done")
    return wavefunctions


