import pytest

from truthtables import TruthTable, PLA


@pytest.fixture(params=["PLA", "TruthTable"])
def table(request):
    if request.param == "PLA":
        input_rows = ["0-0", "001", "10-", "110", "111"]
        output_rows = ["11", "10", "01", "0~", "11"]
        return PLA(input_rows, output_rows)
    elif request.param == "TruthTable":
        return TruthTable(["00", "01", "10", "11", "10", "11", "00", "01"])
