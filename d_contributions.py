#!/usr/bin/env python3

import numpy as np
import itertools

output = "orca_example.out" # output file
match = "ZERO-FIELD SPLITTING" # \n(SPIN-SPIN COUPLING CONTRIBUTION)"

data = []
string = ""

def find_active_space(f):
    """
    Finds active space from Orca MRCI .out file
    """
    electron = "Number of active electrons"
    orbital = "Number of active orbitals"

    nel = 0
    norb = 0

    for line in f:
        if line.startswith(electron):
            nel = line.split()[-1]

        elif line.startswith(orbital):
            norb = line.split()[-1]

    if nel != 0 and norb != 0:
        print("Active space: CAS(", nel, ",", norb, ")")
    else:
        print("Problems with finding active space")
    
def find_ssc(f, cont):

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

    for line in f:
        if line.startswith(match):
            data = itertools.islice(f, n_lines)
            break

    # Print result
    print(match)
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



# ------------------------
#          MAIN
# ------------------------
if __name__ == "__main__":
    with open(output) as f:
        # find_active_space(f)
        print()
        find_ssc(f, "ss")
        print()
        find_ssc(f, "2nd so")
        print()
        find_ssc(f, "effham so")
        print()
        find_ssc(f, "ss and 2nd so")
        print()
        find_ssc(f, "ss and effham so")
        print()
