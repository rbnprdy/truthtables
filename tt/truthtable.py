"""Contains the definition of the TruthTable base class"""
import numpy as np

from utils.pla_utils import read_table


class TruthTable:
        
    def __init__(self, filename=None, inputs=None, outputs=None):
        if filename:
            self.inputs, self.outputs = read_table(filename)
        else:
            # FIXME: Check if inputs are numpy arrays
            if len(inputs.shape) == 1:
                inputs = np.expand_dims(inputs, axis=0)
            if len(outputs.shape) == 1:
                outputs = np.expand_dims(outputs, axis=0)
            self.inputs = inputs
            self.outputs = outputs


    def __getitem__(self, key):
        if not isinstance(key, slice):
            print('he', key)
            inputs = np.expand_dims(self.inputs[key], axis=0)
            outputs = np.expand_dims(self.outputs[key], axis=0)
            return TruthTable(inputs=inputs, outputs=outputs)
        else:
            print(key)
            return TruthTable(inputs=self.inputs[key],
                              outputs=self.outputs[key])

    
    def __iter__(self):
        return iter([TruthTable(inputs=i, outputs=o) for i, o in
                     zip(self.inputs, self.outputs)])


    def __str__(self):
        s = ''
        for i, o in zip(self.inputs, self.outputs):
            s += ''.join(list(str(c) for c in i)).replace('2', '-') + ' '
            s += ''.join(list(str(c) for c in o)).replace('2', '~') + '\n'
        return s.rstrip()

tt = TruthTable(filename='c17.pla')
#print(tt.inputs[0:2])
for t in tt[0:3]:
    print(t)
