"""Classes for representing truth tables"""

import math

import numpy as np


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
        output_num = self.outputs.index(output)
        idxs = []
        for idx, line in enumerate(self):
            if line[output_num] == "1":
                idxs.append(idx)
        return idxs

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
        filename=None,
        input_lines=None,
        output_lines=None,
        inputs=None,
        outputs=None,
        name="ckt",
    ):
        if filename:
            self.input_lines, self.output_lines = read_pla(filename)
        else:
            if not isinstance(input_lines, np.ndarray):
                input_lines = np.asarray(input_lines)
            if not isinstance(output_lines, np.ndarray):
                output_lines = np.asarray(output_lines)
            if len(input_lines.shape) == 1:
                input_lines = np.expand_dims(input_lines, axis=0)
            if len(output_lines.shape) == 1:
                output_lines = np.expand_dims(output_lines, axis=0)
            self.input_lines = input_lines
            self.output_lines = output_lines

        num_inputs = self.num_inputs
        if inputs:
            if num_inputs != len(inputs):
                raise ValueError("Number of inputs must equal log2(number of rows)")
            self.inputs = inputs
        else:
            self.inputs = [f"i{i}" for i in range(num_inputs)]

        num_outputs = self.num_outputs
        if outputs:
            if num_outputs != len(outputs):
                raise ValueError("Number of outputs must equal length of each row")
            self.outputs = outputs
        else:
            self.outputs = [f"o{i}" for i in range(num_outputs)]

        self.name = name

    @staticmethod
    def from_truth_table(table):
        """Create a PLA from a TruthTable."""
        input_lines = []
        output_lines = []
        for idx, line in enumerate(table):
            input_lines.append([int(i) for i in bin(idx)[2:].zfill(table.num_inputs)])
            output_lines.append([int(i) for i in line])
        return PLA(
            input_lines=input_lines,
            output_lines=output_lines,
            inputs=table.inptus,
            outputs=table.outputs,
            name=table.name,
        )

    def __getitem__(self, key):
        return PLA(
            input_lines=self.input_lines[key], output_lines=self.output_lines[key]
        )

    def __iter__(self):
        return iter(
            [
                PLA(input_lines=i, output_lines=o)
                for i, o in zip(self.input_lines, self.output_lines)
            ]
        )

    def __str__(self):
        s = ""
        for i, o in zip(self.input_lines, self.output_lines):
            s += "".join(list(str(c) for c in i)).replace("2", "-") + " "
            s += "".join(list(str(c) for c in o)).replace("2", "~") + "\n"
        return s.rstrip()

    def __eq__(self, other):
        if isinstance(other, PLA):
            return np.array_equal(
                self.input_lines, other.input_lines
            ) and np.array_equal(self.output_lines, other.output_lines)
        return False

    def __add__(self, other):
        return PLA(
            input_lines=np.concatenate(self.input_lines, other.input_lines),
            output_lines=np.concatenate(self.output_lines, other.output_lines),
        )

    @property
    def num_inputs(self):
        return self.input_lines.shape[1]

    @property
    def num_outputs(self):
        return self.output_lines.shape[1]

    @property
    def num_products(self):
        return self.input_lines.shape[0]

    @property
    def entropy(self):
        return entropy([i.split()[-1] for i in str(self).split("\n")])

    @property
    def output_entropy(self):
        entropies = []

        for o in self.output_lines.T:
            entropies.append(entropy(list(o)))
        return entropies

    def onset(self, output):
        """Get the indices for which an output is 1."""
        output_num = self.outputs.index(output)
        return (self.output_lines[:, output_num] == 1).nonzero()[0]

    def input_product(self, line_num):
        """Returns a string representing one line as a product of inputs"""
        terms = []
        for i, val in enumerate(self.input_lines[line_num]):
            if val == 0:
                terms.append("~" + self.inputs[i])
            elif val == 1:
                terms.append(self.inputs[i])
        return " & ".join(terms)

    def to_int(self):
        """Returns numpy arrays representing the inputs and outputs as ints."""
        inputs = np.zeros((self.num_products), dtype=int)
        outputs = np.zeros((self.num_products), dtype=int)
        for line_num, (i, o) in enumerate(zip(self.input_lines, self.output_lines)):
            if 2 in i or 2 in o:
                raise ValueError(
                    "TruthTable cannot have DC bits when " + "converting to int."
                )
            i = "".join(str(val) for val in list(i))
            o = "".join(str(val) for val in list(o))
            inputs[line_num] = int(i, 2)
            outputs[line_num] = int(o, 2)

        return inputs, outputs


def entropy(vals):
    return sum(
        -vals.count(i) / len(vals) * math.log2(vals.count(i) / len(vals))
        for i in set(vals)
    )


class PLAParsingError(Exception):
    pass


def read_pla(path):
    """Read a PLA from a file."""
    num_inputs, num_outputs, num_products = read_pla_info(path)
    inputs = np.empty((num_products, num_inputs), dtype=np.uint8)
    outputs = np.empty((num_products, num_outputs), dtype=np.uint8)
    table_start = 0

    def line_to_list(line):
        """Convert a pla line to a list of ints."""
        lines = []
        for c in line:
            if c == "0":
                lines.append(0)
            elif c == "1":
                lines.append(1)
            elif c in ("-", "~"):
                lines.append(2)
            else:
                raise ValueError
        return lines

    with open(path) as f:
        for line_num, line in enumerate(f):
            line = line.strip()
            # Check if this line specifices a line in the truth table
            if line and line[0] in "10-":
                if table_start == 0:
                    table_start = line_num
                sections = line.split()
                if len(sections) != 2:
                    raise PLAParsingError(
                        f"PLA file {path} line {line_num} contains {len(sections)}"
                        "sections instead of 2."
                    )
                i, o = sections
                if len(i) != num_inputs:
                    raise PLAParsingError(
                        f"PLA file {path} line {line_num} contains the incorrect "
                        "number of inputs."
                    )
                if len(o) != num_outputs:
                    raise PLAParsingError(
                        f"PLA file {path} line {line_num} contains the incorrect "
                        "number of outputs."
                    )
                try:
                    i = line_to_list(i)
                    o = line_to_list(o)
                except ValueError as e:
                    raise PLAParsingError(
                        f"PLA file {path} line {line_num} contains an unexpected "
                        "character."
                    ) from e

                inputs[line_num - table_start] = i
                outputs[line_num - table_start] = o

    return inputs, outputs


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
    with open(path) as f:
        for line in f:
            if line.strip() and line.strip()[0:3] == ".i ":
                num_inputs = int(line.strip().split()[-1])
            elif line.strip() and line.strip()[0:3] == ".o ":
                num_outputs = int(line.strip().split()[-1])
            elif line.strip() and line.strip()[0:3] == ".p ":
                num_products = int(line.strip().split()[-1])

    if not num_inputs:
        raise PLAParsingError("PLA file does not specify the number of inputs.")
    if not num_outputs:
        raise PLAParsingError("PLA file does not specify the number of outputs.")
    if not num_products:
        raise PLAParsingError("PLA file does not specify the a number of products.")

    return num_inputs, num_outputs, num_products
