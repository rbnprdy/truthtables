"""Classes for representing truth tables"""

import math
from itertools import product


class TruthTable:
    """Fully defined truth table as list of bit strings"""

    def __init__(self, rows, inputs=None, outputs=None, name="ckt"):
        num_inputs = math.log(len(rows), 2)
        if not num_inputs.is_integer():
            raise ValueError("Number of rows must be a power of 2")
        num_inputs = int(num_inputs)
        if inputs:
            if num_inputs != len(inputs):
                raise ValueError("Number of inputs must equal log2(number of rows)")
            self.inputs = inputs
        else:
            self.inputs = [f"i{i}" for i in range(num_inputs)]

        num_outputs = len(rows[0])
        if outputs:
            if num_outputs != len(outputs):
                raise ValueError("Number of outputs must equal length of each row")
            self.outputs = outputs
        else:
            self.outputs = [f"o{i}" for i in range(num_outputs)]

        self.rows = rows
        self.name = name

    @staticmethod
    def from_pla(table):
        # Expand DCs
        expanded_input_rows = []
        expanded_output_rows = []
        for input_row, output_row in table:
            # Replace DC outputs with 0
            output_row = output_row.replace("~", "0")
            # Expand DC inputs
            if "-" in input_row:
                dc_idxs = [i for i, val in enumerate(input_row) if val == "-"]
                input_row = list(input_row)
                for vs in product(["0", "1"], repeat=len(dc_idxs)):
                    for idx, v in zip(dc_idxs, vs):
                        input_row[idx] = v
                    expanded_input_rows.append("".join(input_row))
                    expanded_output_rows.append(output_row)
            else:
                expanded_input_rows.append(input_row)
                expanded_output_rows.append(output_row)

        # Set outputs to 0 for input rows that are not in expanded PLA
        input_rows = [
            bin(i)[2:].zfill(table.num_inputs) for i in range(2**table.num_inputs)
        ]
        output_rows = []

        for input_row in input_rows:
            if input_row in expanded_input_rows:
                output_rows.append(
                    expanded_output_rows[expanded_input_rows.index(input_row)]
                )
            else:
                output_rows.append("0" * table.num_outputs)

        return TruthTable(
            output_rows, inputs=table.inputs, outputs=table.outputs, name=table.name
        )

    def __getitem__(self, key):
        return self.rows[key]

    def __iter__(self):
        return iter(self.rows)

    def __len__(self):
        return len(self.rows)

    @property
    def num_inputs(self):
        return len(self.inputs)

    @property
    def num_outputs(self):
        return len(self.outputs)

    def input_str(self, line_num):
        """Get the bit string value of the inputs at a line."""
        return bin(line_num)[2:].zfill(self.num_inputs)

    def onset(self, output):
        """Get the indices for which an output is 1."""
        output_idx = self.outputs.index(output)
        return [i for i, line in enumerate(self) if line[output_idx] == "1"]

    def input_product(self, line_num):
        """Returns a string representing one line as a product of inputs"""
        terms = []
        for i, val in enumerate(self.input_str(line_num)):
            if val == "0":
                terms.append("~" + self.inputs[i])
            else:
                terms.append(self.inputs[i])
        return " & ".join(terms)


class PLA:
    """Represent full featured PLA as numpy arrays."""

    def __init__(
        self,
        input_rows,
        output_rows,
        name="ckt",
        inputs=None,
        outputs=None,
        pla_type="fd",
    ):
        self.input_rows = input_rows
        self.output_rows = output_rows

        self.name = name

        if inputs:
            self.inputs = inputs
        else:
            self.inputs = [f"i{i}" for i in range(self.num_inputs)]

        if outputs:
            self.outputs = outputs
        else:
            self.outputs = [f"o{i}" for i in range(self.num_outputs)]

        self.pla_type = pla_type

    @staticmethod
    def from_file(filename):
        input_rows, output_rows, pla_type = read_pla(filename)
        return PLA(input_rows, output_rows, pla_type=pla_type)

    @staticmethod
    def from_truth_table(table):
        """Create a PLA from a TruthTable."""
        return PLA(
            [bin(i)[2:].zfill(table.num_inputs) for i in range(2**table.num_inputs)],
            table.rows,
            inputs=table.inputs,
            outputs=table.outputs,
            name=table.name,
        )

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.input_rows[key], self.output_rows[key]
        return PLA(self.input_rows[key], self.output_rows[key])

    def __iter__(self):
        return iter([self[i] for i in range(self.num_products)])

    def __str__(self):
        return "\n".join(" ".join(line) for line in self)

    def __add__(self, other):
        return PLA(
            self.input_rows + other.input_rows,
            self.output_rows + other.output_rows,
            inputs=self.inputs,
            outputs=self.outputs,
            name=self.name,
        )

    def __len__(self):
        return len(self.input_rows)

    @property
    def num_inputs(self):
        return len(self.input_rows[0])

    @property
    def num_outputs(self):
        return len(self.output_rows[0])

    @property
    def num_products(self):
        return len(self.input_rows)

    @property
    def entropy(self):
        return entropy([i.split()[-1] for i in str(self).split("\n")])

    @property
    def output_entropies(self):
        return [entropy(o) for o in list(map(list, zip(*self.output_rows)))]

    def onset(self, output):
        """Get the indices for which an output is 1."""
        output_idx = self.outputs.index(output)
        return [i for i, line in enumerate(self.output_rows) if line[output_idx] == "1"]

    def input_product(self, line_num):
        """Returns a string representing one line as a product of inputs"""
        terms = []
        for i, val in enumerate(self.input_rows[line_num]):
            if val == "0":
                terms.append("~" + self.inputs[i])
            elif val == "1":
                terms.append(self.inputs[i])
        return " & ".join(terms)


def entropy(vals):
    return sum(
        -vals.count(i) / len(vals) * math.log2(vals.count(i) / len(vals))
        for i in set(vals)
    )


class PLAParsingError(Exception):
    pass


def read_pla(path):
    """Read a PLA from a file."""
    num_inputs, num_outputs, num_products, pla_type = read_pla_info(path)

    inputs = []
    outputs = []
    with open(path) as f:
        for idx, line in enumerate(f):
            line = line.strip()
            # Check if this line specifices a line in the truth table
            if line and line[0] in "10-":
                sections = line.split()
                if len(sections) != 2:
                    raise PLAParsingError(f"Malformatted line at line {idx}")
                i, o = sections
                if len(i) != num_inputs:
                    raise PLAParsingError(f"Incorrect number of inputs at line {idx}")
                if len(o) != num_outputs:
                    raise PLAParsingError(f"Incorrect number of outputs at line {idx}")
                inputs.append(i)
                outputs.append(o)

    if len(inputs) != num_products:
        raise PLAParsingError("PLA file header mismatches actual number of products")

    return inputs, outputs, pla_type


def read_pla_info(path):
    """Extract information from the header of a pla file

    Parameters
    ----------
    path: str or pathlib.Path
            The path to the file.

    Returns
    -------
    tuple of (int, int, int):
            The number of inputs, the number of outputs, and the number of
            products.
    """
    num_inputs = None
    num_outputs = None
    num_products = None
    pla_type = "fd"
    with open(path) as f:
        for line in f:
            if line.strip() and line.strip()[0:3] == ".i ":
                num_inputs = int(line.strip().split()[-1])
            elif line.strip() and line.strip()[0:3] == ".o ":
                num_outputs = int(line.strip().split()[-1])
            elif line.strip() and line.strip()[0:3] == ".p ":
                num_products = int(line.strip().split()[-1])
            elif line.strip() and line.strip()[0:6] == ".type ":
                pla_type = line.strip().split()[-1].strip()

    if not num_inputs:
        raise PLAParsingError("PLA file does not specify the number of inputs.")
    if not num_outputs:
        raise PLAParsingError("PLA file does not specify the number of outputs.")
    if not num_products:
        raise PLAParsingError("PLA file does not specify the a number of products.")

    return num_inputs, num_outputs, num_products, pla_type
