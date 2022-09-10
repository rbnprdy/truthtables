import pytest

from truthtables import TruthTable


@pytest.fixture
def table():
    return TruthTable(["00", "01", "10", "11"])
