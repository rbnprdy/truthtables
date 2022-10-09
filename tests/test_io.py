import subprocess
from itertools import product

import pytest
import circuitgraph as cg
from circuitsim import CircuitSimulator

import truthtables as tt


@pytest.mark.parametrize("mode", ["case", "sop"])
def test_to_file(mode, table, tmp_path):
    out_file = tmp_path / "out.v"
    syn_file = tmp_path / "syn.v"
    tt.to_file(table, out_file, mode=mode)
    with open(out_file) as f:
        print(f.read())
    subprocess.run(["verilator", "--lint-only", out_file], check=True)
    subprocess.run(
        [
            "yosys",
            "-p",
            f"read_verilog {out_file}; synth; write_verilog -noattr {syn_file}",
        ],
        check=True,
    )
    c = cg.from_file(syn_file)
    sim = CircuitSimulator(c)

    # Enumerate complete truth table to check for correctness
    if isinstance(table, tt.PLA):
        table = tt.TruthTable.from_pla(table)
    for idx, row in enumerate(table):
        inp_str = table.input_str(idx)
        res = sim.simulate(
            [{inp: int(inp_str[i]) for i, inp in enumerate(table.inputs)}]
        )[0]
        assert res == {oup: int(row[i]) for i, oup in enumerate(table.outputs)}
