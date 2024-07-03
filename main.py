import argparse
import numpy as np
import chem_wavefunction

def main():
    parser = argparse.ArgumentParser(description="Reads matrices from an xml file and computes the eigenvalues and eigenfunctions")
    parser.add_argument("input", help="input file in xml format containing the matrices to be analyzed", default="benzene_kekule.xml")
    args = parser.parse_args()
    wavefunctions = chem_wavefunction.read_wavefunctions_from_xml(args.input)

    print("I have read the following wavefunctions:")
    for wf in wavefunctions:
        print("Analyzing wavefunction {}".format(wf.get_name()))
#        print_matrix("Eigenvalues:", np.array([wf.get_eigenvalues()]))
        print_matrix("Eigenfunctions:", wf.get_eigenfunctions())
#        print("Occupation: {}".format(wf.get_occupation()))
#        print("Huckel energy: {}".format(wf.get_huckel_energy()))
#        print_matrix("Overlap matrix with itself:", wf.get_overlap_matrix(wf))
        pass
    
    for wf1 in wavefunctions:
        for wf2 in wavefunctions:
            print_matrix("Overlap between {} and {}:".format(wf1.get_name(), wf2.get_name()), wf1.get_overlap_matrix(wf2))
            print("Overlap wavefunction: {}".format(wf1.get_overlap_wf(wf2)))

def print_matrix(title, matrix, ndigit=2):
    print(title)
    for row in matrix:
        print(" ".join(["{:+.{ndigit}f}".format(x, ndigit=ndigit) for x in row]))

if __name__ == "__main__":
    main()
