import pytest

from truthtables import TruthTable, PLA


@pytest.fixture(params=["PLA", "TruthTable"])
def table(request):
    if request.param == "PLA":
        return PLA(input_lines=[[0, 2], [1, 0], [1, 1]], output_lines=[[1, 0], [0, 1], [1, 1]])
    elif request.param == "TruthTable":
        return TruthTable(["00", "01", "10", "11"])
