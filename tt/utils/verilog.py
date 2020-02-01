"""Utilities for writing a truth table to a verilog file"""

def write_verilog_sop(tt, filename, modulename='ckt'):
    """Writes the truth table to a verilog file by computing the SOP for each
    output"""
    inputs, outputs = _get_io_names(tt.num_inputs, tt.num_outputs)

    with open(filename, 'w') as f:
        f.write(_get_header(inputs, outputs, modulename))

        for output_num, output in enumerate(outputs):
            products = []
            for line in tt.onset(output_num):
                products.append('(' + line.input_product(0) + ')')
            sums = ' | '.join(products)
            f.write('assign ' + output + ' = ' + sums + ';\n')

        f.write('\nendmodule\n')


def write_verilog_case(tt, filename, modulename='ckt'):
    inputs, outputs = _get_io_names(tt.num_inputs, tt.num_outputs)
    
    with open(filename, 'w') as f:
        f.write(_get_header(inputs, outputs, modulename, reg=True))
        f.write('always@({}) begin\n'.format(', '.join(inputs)))
        f.write('\tcasez ({{{}}})\n'.format(', '.join(inputs)))
        for line in tt:
            line_str = str(line)
            input_str, output_str = line_str.split()
            input_str = input_str.replace('-', '?')
            reduced_outputs = [outputs[i] if x != '~' 
                               for i, x in enumerate(output_str)]
            output_str = output_str.replace('~', '')
            f.write('\t\t{}\'b{} : '.format(tt.num_inputs, input_str))
            f.write('{{{}}} = '.format(', '.join(reduced_outputs)))
            f.write('{}\'b{};\n'.format(tt.num_outputs, output_str))
        #f.write('\t\tdefault : {{{}}} = '.format(', '.join(outputs)))
        f.write('{}\'d0;\n'.format(tt.num_outputs))
        f.write('\tendcase\nend\nendmodule')


def _get_io_names(num_inputs, num_outputs):
    inputs = ['i{}'.format(i) for i in range(num_inputs)]
    outputs = ['o{}'.format(i) for i in range(num_outputs)]
    return inputs, outputs


def _get_header(inputs, outputs, modulename, reg=False):
    s = 'module {}({});\n\n'.format(
            modulename, ', '.join(inputs + outputs))
    s += 'input {};\n'.format(', '.join(inputs))
    if reg:
        s += 'output reg {};\n\n'.format(', '.join(outputs))
    else:
        s += 'output {};\n\n'.format(', '.join(outputs))
    return s

