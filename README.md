# TruthTables

A library for working with truth tables in python.

To install, run `pip install .`  in the root directory. Note: adding the `-e` flag will make the package editable.

For fully defined truth tables (every row is represented, no Don't Care values), use the `TruthTable` class, which is simply a wrapper around a list of bit strings representing the outputs at each row.

```python
import truthtables as tt


rows = ["00", "01", "10", "11"]
table = tt.TruthTable(rows)

for idx, oup_str in enumerate(table):
    print(table.input_str(idx), oup_str)

tt.to_file(table, "example_table.v")
```

More complicated tables can be represented using the `PLA` class which, at its core, contains two numpy arrays: `input_lines` and `output_lines`. Both are 2D matrices where each row represents a line in the truth table. DCs are represented by the number 2. `PLA` objects also support slicing and iteration, both of which return smaller `PLA` objects.

Some helpful properties that can be computed for truthtables are added as member functions or properties.

This library also contains utilities for reading and writing from PLA files and writing to verilog files.
