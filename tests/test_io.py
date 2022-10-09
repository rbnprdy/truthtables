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
    for idx, row in enumerate(table):
        if isinstance(table, tt.TruthTable):
            inp_str = table.input_str(idx)
            res = sim.simulate(
                [{inp: int(inp_str[i]) for i, inp in enumerate(table.inputs)}]
            )[0]
            assert res == {oup: int(row[i]) for i, oup in enumerate(table.outputs)}
        else:
            vector = {inp: row[0][i] for i, inp in enumerate(table.inputs)}
            set_inputs = {k: bool(v) for k, v in vector.items() if v != 2}
            unset_inputs = [k for k, v in vector.items() if v == 2]
            if unset_inputs:
                vectors = []
                for i, vs in enumerate(
                    product([False, True], repeat=len(unset_inputs))
                ):
                    vectors.append(
                        {**{k: v for k, v in zip(unset_inputs, vs)}, **set_inputs}
                    )
            else:
                vectors = [set_inputs]
            for res in sim.simulate(vectors):
                assert res == {
                    oup: bool(row[1][i]) for i, oup in enumerate(table.outputs)
                }
