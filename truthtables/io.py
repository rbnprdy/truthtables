"""Functions for reading/writing truth tables"""

from pathlib import Path
from datetime import datetime

from truthtables import TruthTable, PLA


def to_file(table, filename, fmt=None, mode="case"):
    """Write a truthtable to a file.

    Parameters
    ----------
    table: TruthTable or PLA
    filename: str or Pathlib.path
    fmt: str
            If defined, describes what file type to write.
            Either "verilog" or "pla". If not defined,
            inferred from extension of `filename`
    mode: str
            If writing a veirlog file, describes how to represent the
            truth table. Either "case" or "sop"
    """
    filename = Path(filename)
    if not fmt:
        if filename.suffix == ".v":
            fmt = "verilog"
        elif filename.suffix == ".pla":
            fmt = "pla"
        else:
            raise ValueError(
                f"Unable to infer fmt from filename suffix: '{filename.suffix}'"
            )

    if fmt == "verilog":
        if mode == "case":
            write_verilog_case(table, filename)
        elif mode == "sop":
            write_verilog_sop(table, filename)
        else:
            raise ValueError(f"Unknown mode: '{mode}'")
    elif fmt == "pla":
        write_pla(table, filename)
    else:
        raise ValueError(f"Unknown fmt: '{fmt}'")


def write_verilog_sop(table, filename):
    """Write a truth table to a verilog file using SOP assignemnts."""
    with open(filename, "w") as f:
        f.write(_get_header(table.inputs, table.outputs, table.name))

        for output in table.outputs:
            products = []
            for line_idx in table.onset(output):
                products.append("( " + table.input_product(line_idx) + " )")
            if products:
                sums = " | ".join(products)
                f.write("assign " + output + " = " + sums + " ;\n")

        f.write("\nendmodule\n")


def get_case_block(table: TruthTable):
    s = "always@(*) begin\n"
    outputs = " , ".join(table.outputs)
    if isinstance(table, TruthTable):
        s += f"\tcase ({{ {' , '.join(table.inputs)} }})\n"
        for idx, oup_line in enumerate(table):
            inp_line = bin(idx)[2:].zfill(table.num_inputs)
            s += f"\t\t{table.num_inputs}'b{inp_line} : "
            s += f"{{ {outputs} }} = {table.num_outputs}'b{oup_line};\n"
    elif isinstance(table, PLA):
        raise NotImplementedError
    s += "\tendcase\nend\n"
    return s


def write_verilog_case(table: TruthTable, filename):
    """Write a truth table to a verilog file using a case statement."""
    with open(filename, "w") as f:
        f.write(_get_header(table.inputs, table.outputs, table.name, reg=True))
        f.write(get_case_block(table))
        f.write("\nendmodule")


def _get_header(inputs, outputs, name, reg=False):
    s = f"// Written by truthtables on {datetime.now()}\n"
    s += f"module {name}( {' , '.join(inputs + outputs)} );\n\n"
    s += f"input {' , '.join(inputs)} ;\n"
    if reg:
        s += f"output reg {' , '.join(outputs)} ;\n\n"
    else:
        s += f"output {' , '.join(outputs)} ;\n\n"
    return s


def write_pla(table, path):
    """Writes a truth table to a pla file."""
    if isinstance(table, TruthTable):
        table = PLA.from_truth_table(table)
    with open(path, "w") as f:
        f.write(f"# Written by truthtables on {datetime.now()}\n")
        f.write(f".i {table.num_inputs}\n")
        f.write(f".o {table.num_outputs}\n")
        f.write(f".ilb {' '.join(table.inputs)}\n")
        f.write(f".ob {' '.join(table.outputs)}\n")
        f.write(f".type {table.pla_type}\n")
        f.write(f".p {table.num_products}\n")
        f.write(str(table))
        f.write("\n")
        f.write(".end")
