"""Functions for generating truth tables"""
import random

from truthtables import TruthTable


def random_table(num_inputs, num_outputs, bias=0.5):
    """Generate a random table.

    Parameters
    ----------
    num_inputs: int
            The number of inputs.
    num_outputs: int
            The number of outputs.
    bias: float
            The bias for the random number generator.
            A bias of 0.5 (default) generates 0s and 1s with equal
            probability. A bias of 1 generates all 1s.

    Returns
    -------
    TruthTable
            The random table.
    """
    rows = []
    val = 0
    for _ in range(2**num_inputs):
        val = 0
        for _ in range(num_outputs):
            x = [0, 1][random.random() < bias]
            val = (val << 1) | x
        rows.append(bin(val)[2:].zfill(num_outputs))
    return TruthTable(rows)
