import math

from truthtables import TruthTable


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
