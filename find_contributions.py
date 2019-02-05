#!/usr/bin/env python3

import numpy as np
import itertools

output = "orca_gD_mrci_example.out" # output file
match = "ZERO-FIELD SPLITTING" # \n(SPIN-SPIN COUPLING CONTRIBUTION)"

data = []
string = ""

def find_active_space(path):
    """
    Finds active space from Orca MRCI .out file
    """
    electron = "Number of active electrons"
    orbital = "Number of active orbitals"

    nel = 0
    norb = 0

    with open(path) as f:
        for line in f:
            if line.startswith(electron):
                nel = line.split()[-1]

            elif line.startswith(orbital):
                norb = line.split()[-1]

    if nel != 0 and norb != 0:
        print("Active space: CAS(", nel, ",", norb, ")")
    else:
        print("Problems with finding active space")
    

def print_data(data):
    """
    Prints found data.
    """
    for d in data:
        if str(d) != "\n":
            try:
                float(d.split()[0])
                raw_data_array = [float(i) for i in d.split()]
                print("{0:.6f}".format(raw_data_array[0]),
                      "{0:.6f}".format(raw_data_array[1]),
                      "{0:.6f}".format(raw_data_array[2])
                       ) 
                
            except ValueError:
                print(d.strip("\n"))


def find_D(cont, path):
    """
    Finds D-tensors contributions in orca .out file.

    :param f: opened file .out
    :param cont: contribution to search
    """

    n_lines = 21 # lines after match

    if cont == "ss":
        match = "(SPIN-SPIN COUPLING CONTRIBUTION)"
        n_lines = 25
    elif cont == "2nd so":
        match = "(2ND ORDER SPIN-ORBIT COUPLING CONTRIBUTION)"
        n_lines = 36
    elif cont == "effham so":
        match = "(EFFECTIVE HAMILTONIAN SPIN-ORBIT COUPLING CONTRIBUTION)"
    elif cont == "ss and 2nd so":
        match = "(SPIN-SPIN AND 2ND ORDER SPIN-ORBIT COUPLING CONTRIBUTIONS)"
    elif cont == "ss and effham so":
        match = "(SPIN-SPIN AND EFFECTIVE HAMILTONIAN SPIN-ORBIT COUPLING CONTRIBUTION)"
    else:
        match = "Contribution not found"
        data = []

    with open(path) as f:
        for line in f:
            if line.startswith(match):
                data = itertools.islice(f, n_lines)
                break

        # Print result
        print(match)
        print_data(data)


def find_g(cont, path):
    """
    Finds g-tensor components from orca .out file
    """

    n_lines = 17

    # Orca spin orbit calculation
    if cont == "soc":
        print("\n------------------------------------")
        print("ORCA SPIN-ORBIT COUPLING CALCULATION")
        print("------------------------------------\n")
        match = "ELECTRONIC G-MATRIX"
    elif cont == "s-cont":
        match = "ELECTRONIC G-MATRIX: S contribution"
    elif cont == "l-cont":
        match = "ELECTRONIC G-MATRIX: L contribution"
    elif cont == "effham":
        match = "ELECTRONIC G-MATRIX FROM EFFECTIVE HAMILTONIAN"
    elif cont == "sos":
        print("\n---------------------------")
        print("SUM OVER STATES CALCULATION")
        print("---------------------------\n")
        match = "ELECTRONIC G-MATRIX"
    else:
        data = []

    print(match)

    with open(path) as f:
        for line in f:
            if line.startswith(match):
                data = itertools.islice(f, n_lines)
                break

        print_data(data)



# ------------------------
#          MAIN
# ------------------------
if __name__ == "__main__":
    print()
    find_g("soc", output)
    print()
    find_g("l-cont", output)
    print()
    find_g("s-cont", output)
    print()
    find_g("effham", output)
    print()
    find_g("sos", output)
    print()
    find_active_space(output)
    print()
    find_D("ss", output)
    print()
    find_D("ss", output)
    print()
    find_D("2nd so", output)
    print()
    find_D("effham so", output)
    print()
    find_D("ss and 2nd so", output)
    print()
    find_D("ss and effham so", output)
    print()
