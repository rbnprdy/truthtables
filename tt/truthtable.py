"""Contains the definition of the TruthTable base class"""
import numpy as np

from .utils.pla import read_pla


class TruthTable:
        
    def __init__(self, filename=None, input_lines=None, output_lines=None):
        if filename:
            self.input_lines, self.output_lines = read_pla(filename)
        else:
            if not isinstance(input_lines, np.ndarray):
                input_lines = np.asarray(input_lines)
            if not isinstance(output_lines, np.ndarray):
                output_lines = np.asarray(output_lines)
            if len(input_lines.shape) == 1:
                input_lines = np.expand_dims(input_lines, axis=0)
            if len(output_lines.shape) == 1:
                output_lines = np.expand_dims(output_lines, axis=0)
            self.input_lines = input_lines
            self.output_lines = output_lines


    def __getitem__(self, key):
        return TruthTable(input_lines=self.input_lines[key],
                          output_lines=self.output_lines[key])

    
    def __iter__(self):
        return iter([TruthTable(input_lines=i, output_lines=o) for i, o in
                     zip(self.input_lines, self.output_lines)])


    def __str__(self):
        s = ''
        for i, o in zip(self.input_lines, self.output_lines):
            s += ''.join(list(str(c) for c in i)).replace('2', '-') + ' '
            s += ''.join(list(str(c) for c in o)).replace('2', '~') + '\n'
        return s.rstrip()


    @property
    def num_inputs(self):
        return self.input_lines.shape[1]

    
    @property
    def num_outputs(self):
        return self.output_lines.shape[1]

    
    @property
    def num_products(self):
        return self.input_lines.shape[0]


    def onset(self, output_num):
        """Returns a truth table with just the entries where output
        `output_num` is 1"""
        onset_idx = (self.output_lines[:,output_num] == 1).nonzero()
        return TruthTable(input_lines=self.input_lines[onset_idx],
                          output_lines=self.output_lines[onset_idx])


    def input_product(self, line_num, input_lables=None):
        """Returns a string representing one line as a product of inputs"""
        if not input_lables:
            input_labels = ['i{}'.format(i) for i in range(self.num_inputs)]
        terms = []
        for i, val in enumerate(self.input_lines[line_num]):
            if val == 0:
                terms.append('~' + input_labels[i])
            elif val == 1:
                terms.append(input_labels[i])
        return ' & '.join(terms)

    
    def to_int(self):
        """Returns two 1D numpy arrays representing the inputs and outputs as
        integer values. Raises a ValueError if a DC bit is found."""
        inputs = np.zeros((self.num_products), dtype=int)
        outputs = np.zeros((self.num_products), dtype=int)
        for line_num, (i, o) in enumerate(
                zip(self.input_lines, self.output_lines)):
            if 2 in i or 2 in o:
                raise ValueError('TruthTable cannot have DC bits when ' +
                                  'converting to int.')
            i = ''.join(str(val) for val in list(i))
            o = ''.join(str(val) for val in list(o))
            inputs[line_num] = int(i, 2)
            outputs[line_num] = int(o, 2)

        return inputs, outputs

