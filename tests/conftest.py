import pytest

from truthtables import TruthTable, PLA


@pytest.fixture(params=["PLA", "TruthTable"])
def table(request):
    if request.param == "PLA":
        return PLA(["0-", "10", "11"], ["10", "01", "11"])
    elif request.param == "TruthTable":
        return TruthTable(["00", "01", "10", "11"])
