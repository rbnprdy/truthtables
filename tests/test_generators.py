from truthtables import random_table


def test_random_table():
    num_inputs = 4
    num_outputs = 6
    table = random_table(num_inputs, num_outputs)
    assert len(table) == 2**num_inputs
    for row in table:
        assert len(row) == num_outputs


def test_bias():
    num_inputs = 4
    num_outputs = 6
    table = random_table(num_inputs, num_outputs, bias=0)
    assert len(table) == 2**num_inputs
    for row in table:
        assert len(row) == num_outputs
        assert row == "0" * 6

    table = random_table(num_inputs, num_outputs, bias=1)
    assert len(table) == 2**num_inputs
    for row in table:
        assert len(row) == num_outputs
        assert row == "1" * 6
