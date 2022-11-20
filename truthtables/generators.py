"""Functions for generating truth tables"""

import random
import ast

from truthtables import TruthTable

def file_table(filename, num_inputs, num_outputs, bias=0.5):

    dict_list = []
    rows = []

    f = open(filename, 'r')
    lines = f.readlines()

    for line in lines:
        d = line.strip()
        d = d.replace(" ", "")
        d = d.replace("\n", "")
        d = d.replace("{", "")
        d = d.replace("}", "")
        #print("Hello")
        #print(d)
        data = dict(item.split(":") for item in d.split(","))
        #for item in d.split(","):
        #    print(item.split(":"))
        dict_list.append(data)

    num_input_combo = len(dict_list)
    num_outputs = len(dict_list[0])

    for i in range(num_input_combo): # loop through dict_list
        val = 0
        rand_val = 0
        for key in dict_list[i]:
            #print(type(dict_list[i][key]))
            if (dict_list[i][key] == "False"):
                sv = 0
            else:
                sv = 1
            val = (val << 1) | sv
            x = [0, 1][random.random() < bias]
            #rand_val = (rand_val << 1) | x
        #val = (val ^ rand_val)
        rows.append(bin(val)[2:].zfill(num_outputs))

    return TruthTable(rows)

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
