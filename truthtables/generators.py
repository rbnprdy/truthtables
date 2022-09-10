"""Functions for generating truth tables"""

import random

from truthtables import TruthTable


def random_table(num_inputs, num_outputs):
    lines = []
    for _ in range(2**num_inputs):
        lines.append(bin(random.getrandbits(num_outputs))[2:].zfill(num_outputs))
    return TruthTable(lines)
