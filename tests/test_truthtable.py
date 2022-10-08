import math

import numpy as np

from truthtables import TruthTable, PLA


def test_basic_truthtable():
    rows = ["00", "01", "10", "11"]
    table = TruthTable(rows)
    assert table.name == "ckt"
    assert len(set(table.inputs)) == int(math.log2(len(rows)))
    assert len(set(table.outputs)) == len(rows[0])
    assert table.num_inputs == int(math.log2(len(rows)))
    assert table.num_outputs == len(rows[0])

    for table_row, row in zip(table, rows):
        assert table_row == row

    assert table[-1] == rows[-1]
    assert table.onset(table.outputs[0]) == [2, 3]
    assert table.onset(table.outputs[1]) == [1, 3]

    assert table.input_product(0) == "~i0 & ~i1"
    assert table.input_product(1) == "~i0 & i1"
    assert table.input_product(2) == "i0 & ~i1"
    assert table.input_product(3) == "i0 & i1"

def test_pla():
    input_lines = [[0, 2], [1, 0], [1, 1]]
    output_lines = [[1, 0], [0, 1], [1, 1]]
    table = PLA(input_lines=input_lines, output_lines=output_lines)
    assert table.num_inputs == 2
    assert table.num_outputs == 2
    assert np.array_equal(np.asarray(input_lines), table.input_lines)
    assert np.array_equal(np.asarray(output_lines), table.output_lines)

    assert table.inputs == ["i0", "i1"]
    assert table.outputs == ["o0", "o1"]

    assert table.onset("o0").tolist() == [0, 2]