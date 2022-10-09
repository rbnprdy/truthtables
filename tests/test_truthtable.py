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
    input_rows = ["0-", "10", "11"]
    output_rows = ["10", "01", "11"]
    table = PLA(input_rows, output_rows)
    assert table.num_inputs == 2
    assert table.num_outputs == 2
    assert np.array_equal(np.asarray(input_rows), table.input_rows)
    assert np.array_equal(np.asarray(output_rows), table.output_rows)

    assert table.inputs == ["i0", "i1"]
    assert table.outputs == ["o0", "o1"]

    assert table.onset("o0") == [0, 2]


def test_conversion():
    input_rows = ["0-0", "001", "10-", "110", "111"]
    output_rows = ["11", "10", "01", "0~", "11"]
    pla = PLA(input_rows, output_rows)
    table = TruthTable.from_pla(pla)
    assert table.rows == ["11", "10", "11", "00", "01", "01", "00", "11"]
