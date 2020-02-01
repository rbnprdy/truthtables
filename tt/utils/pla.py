"""Utilities for working with pla files in python"""
from datetime import datetime

import numpy as np


class PLAParsingError(Exception):
    pass


def read_pla(path):
    """Reads the pla file specified by `path` into a numpy array of uints.
    DC is represented by the number 2.
 
    Raises a PLAParsingError if the pla file was maleformatted."""
    num_inputs, num_outputs, num_products = read_pla_info(path)
    inputs = np.empty((num_products, num_inputs), dtype=np.uint8)
    outputs = np.empty((num_products, num_outputs), dtype=np.uint8)
    tt_start = 0
    with open(path) as f:
        for line_num, line in enumerate(f):
            line = line.strip()
            # Check if this line specifices a line in the truth table
            if line and line[0] in '10-':
                if tt_start == 0:
                    tt_start = line_num
                l = line.split()
                if len(l) != 2:
                    raise PLAParsingError(
                        'PLA file {} line {} '.format(path, line_num) +
                        'contains {} sections instead of 2.'.format(len(l)))
                i = l[0]
                o = l[1]
                if len(i) != num_inputs:
                    raise PLAParsingError(
                        'PLA file {} line {} '.format(path, line_num) +
                        'contains the incorrect number of inputs.')
                if len(o) != num_outputs:
                    raise PLAParsingError(
                        'PLA file {} line {} '.format(path, line_num) +
                        'contains the incorrect number of outputs.')
                try:
                    i = _line_to_list(i)
                    o = _line_to_list(o)
                except ValueError:
                    raise PLAParsingError(
                        'PLA file {} line {} '.format(path, line_num) +
                        'contains an unexpected character.')

                inputs[line_num-tt_start] = i
                outputs[line_num-tt_start] = o

    return inputs, outputs


def read_pla_info(path):
    """Returns a tuple with information about the pla file specified by
    `path`. Specifically: the number of inputs, the number of outputs,
    and the number of products."""
    with open(path) as f:
        reset_defined = False
        for line in f:
            if line.strip() and line.strip()[0:3] == '.i ':
                num_inputs = int(line.strip().split()[-1])
            elif line.strip() and line.strip()[0:3] == '.o ':
                num_outputs = int(line.strip().split()[-1])
            elif line.strip() and line.strip()[0:3] == '.p ':
                num_products = int(line.strip().split()[-1])
    
    if not num_inputs:
        raise PLAParsingError('PLA file {} does not specify '.format(path) +
                               'the number of inputs.')
    if not num_outputs:
        raise PLAParsingError('PLA file {} does not specify '.format(path) +
                               'the number of outputs.')
    if not num_products:
        raise PLAParsingError('PLA file {} does not specify '.format(path) +
                               'the a number of products.')
    
    return num_inputs, num_outputs, num_products


def write_pla(tt, path, pla_type=None):
    """Writes a truth table the pla file specified by `path`."""
    with open(path, 'w') as f:
        f.write('# Written by pla_utils on {}\n'.format(datetime.now()))
        f.write('.i {}\n'.format(tt.num_inputs))
        f.write('.o {}\n'.format(tt.num_outputs))
        f.write('.ilb {}\n'.format(
            ' '.join('i{}'.format(i) for i in range(tt.num_inputs))))
        f.write('.ob {}\n'.format(
            ' '.join('o{}'.format(i) for i in range(tt.num_outputs))))
        if pla_type:
            f.write('.type {}\n'.format(pla_type))
        f.write('.p {}\n'.format(tt.num_products))
        f.write(str(tt))
        f.write('\n')
        f.write('.end')


def _line_to_list(line):
    """Converts a pla line to a list of ints.
    
    Raises a ValueError if it encounters an unexpected character."""
    l = []
    for c in line:
        if c == '0':
            l.append(0)
        elif c == '1':
            l.append(1)
        elif c == '-' or c == '~':
            l.append(2)
        else:
            raise ValueError
    return l

