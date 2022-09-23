"""Functions for generating truth tables"""

import random

from truthtables import TruthTable

# add bias (between 0 and 1)
def random_table(num_inputs, num_outputs, bias):
    lines = []

    for _ in range(2**num_inputs):
        for a in range(num_outputs):
            x = random.random()
            if (x > bias):
                lines.append(1)
            else:
                lines.append(0)
        # generates a random number with num_outputs # of bits
        # cuts off "0b" because using bin function
        # zfill adds 0 until num_bits is full
        #lines.append(bin(random.getrandbits(num_outputs))[2:].zfill(num_outputs))
    return TruthTable(lines)
