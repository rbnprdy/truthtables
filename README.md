# Truth Tables

A library for working with truth tables in python.

To install, run `pip install .`  in the root directory. Note: adding the `-e` flag will make the package editable.

Basic manipulations are achieved by instantiating and modifying `TruthTable` objects.
At its core, the TruthTable class contains two numpy arrays: `input_lines` and `output_lines`. Both are 2D matrices where each row represents a line in the truth table. DCs are represented by the number 2. `TruthTables` support slicing and iteration, both of which return smaller `TruthTable` objects.

Helpful properties that can be computed for truthtables are added as member functions or properties on an as needed basis, though the goal is to keep this library relatively generic.

This library also contains utilities for reading and writing from PLA files, and writing to verilog files.
