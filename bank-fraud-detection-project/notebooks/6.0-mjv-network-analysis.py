import marimo

__generated_with = "0.14.16"
app = marimo.App(width="medium")


@app.cell
def _(mo):
    mo.md(
        r"""
    # 6.0 - Network Analysis of Fraudulent Transactions

    _by Michael Joshua Vargas_
    """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""## Import relevant libraries""")
    return


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import numpy as np
    import networkx as nx
    from pyvis.network import Network
    import os
    import sys
    from pathlib import Path
    return Path, mo, os, sys


@app.cell
def _(mo):
    mo.md(r"""## Path setup""")
    return


@app.cell
def _(Path, os, sys):
    # This setup ensures the script can find the bank_fraud package
    try:
        # This works when running as a script
        script_path = Path(__file__).resolve()
    except NameError:
        # Fallback for interactive environments where __file__ might not be defined
        script_path = Path(os.getcwd())

    # Navigate up 2 levels from `.../notebooks/script.py` to the project root
    project_root = script_path.parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    from bank_fraud.config import PROCESSED_DATA_DIR, RAW_DATA_DIR, REPORTS_DIR
    return


if __name__ == "__main__":
    app.run()
