from tempfile import TemporaryDirectory
from pathlib import Path
import subprocess

from truthtables import PLA, to_file


def minimize(table):
    """Use espresso to minimize a truth table.

    Parameters
    ----------
    table: TruthTable or PLA
            The table to minimize.

    Returns
    -------
    PLA
            The minimized table.
    """
    with TemporaryDirectory(prefix="truthtables_minimize") as d:
        d = Path(d)
        input_file = d / "in.pla"
        output_file = d / "out.pla"
        to_file(table, input_file)
        with open(output_file, "w+") as f:
            try:
                subprocess.run(["espresso", str(input_file)], stdout=f, check=True)
            except subprocess.CalledProcessError as e:
                f.seek(0)
                raise ValueError(
                    f"Calling espresso failed. Espresso output:\n\n{f.read()}"
                ) from e
        table_out = PLA.from_file(output_file)
    return table_out
