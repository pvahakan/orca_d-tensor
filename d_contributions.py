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
    
def find_ssc(f):
    match = "(SPIN-SPIN COUPLING CONTRIBUTION)"
    for line in f:
        if line.startswith(match):
            data = itertools.islice(f, 25)
            break

    print(match)
    for d in data:
        if str(d) != "\n":
            try:
                float(d.split()[0])
                raw_data_array = [float(i) for i in d.split()]
                print(raw_data_array[0],raw_data_array[1],raw_data_array[2])
                
            except ValueError:
                print(d.strip("\n"))



# ------------------------
#          MAIN
# ------------------------
if __name__ == "__main__":
    with open(output) as f:
        # find_active_space(f)
        find_ssc(f)

