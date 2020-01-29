"""Utilities for writing a truth table to a verilog file"""

def write_verilog_sop(tt, filename, modulename='ckt'):
    """Writes the truth table to a verilog file by computing the SOP for each
    output"""
    inputs = ['i{}'.format(i) for i in range(tt.num_inputs)]
    outputs = ['o{}'.format(i) for i in range(tt.num_outputs)]

    with open(filename, 'w') as f:
        
        f.write('module {}({});\n\n'.format(
            modulename, ', '.join(inputs + outputs)))
        f.write('input {};\n'.format(', '.join(inputs)))
        f.write('output {};\n\n'.format(', '.join(outputs)))

        for output_num, output in enumerate(outputs):
            products = []
            for line in tt.onset(output_num):
                products.append('(' + line.input_product(0) + ')')
            sums = ' | '.join(products)
            f.write('assign ' + output + ' = ' + sums + ';\n')

        f.write('\nendmodule\n')
