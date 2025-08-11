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
    return Path, mo, os, pd, sys


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
    return (project_root,)


@app.cell
def _(mo, pd, project_root):
    # --- 1. Load and Prepare Data ---

    # Define the path to the network data
    network_data_path = project_root / "data_network" / "raw" / "df_network.csv"

    # Load the dataset WITHOUT parsing dates initially
    df = pd.read_csv(network_data_path)

    # --- Data Cleaning ---
    # 1. Clean column names (lowercase and replace spaces with underscores)
    df.columns = df.columns.str.lower().str.replace(" ", "_")

    # 2. Convert transaction_date to datetime objects
    df["transaction_date"] = pd.to_datetime(
        df["transaction_date"], errors="coerce"
    )

    # 3. Convert transaction_amount to numeric, coercing errors
    df["transaction_amount"] = pd.to_numeric(
        df["transaction_amount"], errors="coerce"
    )

    # 4. Convert transaction_type to string to handle mixed types
    df["transaction_type"] = df["transaction_type"].astype(str)

    # --- Validation and Summary ---
    summary_md = f"""
    ### Data Loading and Cleaning Summary
    - **Shape of the data:** {df.shape}
    - **Date range:** {df["transaction_date"].min()} to {df["transaction_date"].max()}
    - **Columns:** {", ".join(df.columns)}
    """

    mo.md(summary_md)
    return (df,)


@app.cell
def _(mo):
    mo.md(r"""## Define Interactive Filters""")
    return


@app.cell
def ui_controls_for_filtering(df, mo):
    # --- UI Controls for Filtering ---

    # 1. Amount Range Slider
    min_amount = float(df['transaction_amount'].min())
    max_amount = float(df['transaction_amount'].max())
    min_amount_input = mo.ui.number(
        value=min_amount,
        label='Min Amount:'
    )

    max_amount_input = mo.ui.number(
        value=max_amount,
        label='Max Amount:'
    )

    # 2. Transaction Type Dropdown
    # The df['transaction_type'] is already converted to string in the data prep cell
    txn_types = ['All'] + sorted(df['transaction_type'].unique().tolist())
    type_dropdown = mo.ui.dropdown(
        options=txn_types,
        value='All',
        label='Transaction Type:'
    )

    # 3. Date Range Picker
    min_date = df['transaction_date'].min()
    max_date = df['transaction_date'].max()
    start_date = mo.ui.date(
        value=min_date.strftime('%Y-%m-%d'),
        label='Start Date:'
    )
    end_date = mo.ui.date(
        value=max_date.strftime('%Y-%m-%d'),
        label='End Date:'
    )

    # Group all the controls together for a clean layout
    controls = mo.vstack([
        mo.hstack([min_amount_input, max_amount_input], justify='start'),
        type_dropdown,
        mo.hstack([start_date, end_date], justify='start')
    ])

    # Explicitly output the controls object to render it in the UI.
    controls

    # Return the handles to the UI elements so they can be used by other cells.
    return (
        end_date,
        max_amount_input,
        min_amount_input,
        start_date,
        type_dropdown,
    )


@app.cell
def _(mo):
    mo.md(r"""## Filter Data Dynamically""")
    return


@app.cell
def _(
    df,
    end_date,
    max_amount_input,
    min_amount_input,
    mo,
    pd,
    start_date,
    type_dropdown,
):
    # Get the current values from the UI controls
    min_amt = min_amount_input.value
    max_amt = max_amount_input.value
    selected_type = type_dropdown.value
    selected_start = pd.to_datetime(start_date.value)
    selected_end = pd.to_datetime(end_date.value)

    # Start with the original DataFrame
    filtered_df = df

    # Apply the transaction type filter
    if selected_type != 'All':
        filtered_df = filtered_df[filtered_df['transaction_type'] == selected_type]

    # Apply the date range filter
    # We also handle potential NaT (Not a Time) values in the transaction_date
    if pd.notna(selected_start) and pd.notna(selected_end):
        filtered_df = filtered_df[
            filtered_df['transaction_date'].between(selected_start, selected_end)
            ]

    # Apply the amount range filter
    # Handle potential NaN values in the amount column
    filtered_df = filtered_df[
        filtered_df['transaction_amount'].between(min_amt, max_amt)
        ]

    # Display the share of the filtered data as a status updated
    mo.md(f"**Filtered Data:** {len(filtered_df)} rows out of {len(df)} total rows.")

    # Return the filtered_df so it can be used by other cells
    filtered_df
    return


if __name__ == "__main__":
    app.run()
