import truthtables as tt


def test_minimize():
    table = tt.TruthTable(["00", "00", "11", "11"])
    table_min = tt.minimize(table)
    assert table_min.input_rows == ["1-"]
    assert table_min.output_rows == ["11"]
