"""Functions for generating truth tables"""

import random

from truthtables import TruthTable

# add bias (between 0 and 1)
def random_table(num_inputs, num_outputs, bias):
    lines = []
    val = 0
    for _ in range(2**num_inputs):
        val = 0
        for a in range(num_outputs):
           # bias = 0 => use all 1s
            x = [0, 1][random.randrange(0, 10) > bias]
            val = (val << 1) or x
        lines.append(bin(val)[2:].zfill(num_outputs))
        # generates a random number with num_outputs # of bits
        # cuts off "0b" because using bin function
        # zfill adds 0 until num_bits is full
        # lines.append(bin(random.getrandbits(num_outputs))[2:].zfill(num_outputs))
    return TruthTable(lines)