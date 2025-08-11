# Active Context

## Current work focus

*   **Phase 6: Network Analysis - Planning Graph Visualization.**

## Recent changes

*   **Completed Interactive Filtering:** Implemented dynamic, user-driven filters for transaction amount, type, and date in the `6.0-mjv-network-analysis.py` Marimo notebook.
*   **Finalized Network Graph Plan:** Defined a detailed, three-phase plan for constructing and visualizing the transaction network graph. The plan specifies a multi-level graph structure (accounts and banks) and a reactive implementation using `networkx` and `pyvis`.

## Next steps

**Phase 1: Reactive Graph Construction**
*   Create a new Marimo cell that takes the `filtered_df` as input to dynamically build the graph structure using `networkx`.
*   **Initialize Graph:** Start with an empty `networkx.DiGraph`.
*   **Add Nodes & Edges:** For each transaction in `filtered_df`:
    *   Add nodes for `from_account`, `to_account`, and the relevant bank(s), assigning a `type` attribute ('account' or 'bank').
    *   **Intra-bank logic:** If `source_bank_name` equals `destination_bank_name`, create edges: `account -> bank -> account`.
    *   **Inter-bank logic:** If banks differ, create edges: `account -> bank -> other_bank -> account`.
*   **Output:** The cell will return the constructed `networkx` graph object.

**Phase 2: Node and Edge Styling**
*   Create a second cell that takes the graph and applies visual styles.
*   **Node Styling:**
    *   **Color:** Differentiate node types (e.g., blue for accounts, red for banks).
    *   **Size:** Scale node size by degree (number of connections) to highlight hubs.
*   **Edge Styling:**
    *   **Width:** Vary edge thickness based on `transaction_amount`.
    *   **Hover Info:** Add tooltips to edges to show transaction amount and date.

**Phase 3: Visualization and Marimo Integration**
*   Create a final cell to render the styled graph using `pyvis`.
*   **Render with Pyvis:** Load the `networkx` graph into a `pyvis.Network` object, configured with interactive physics.
*   **Embed in Marimo:** Save the graph as a temporary HTML file and use `mo.iframe` to embed it into the notebook output, ensuring full reactivity with the filters.

## Active decisions and considerations

*   Using a Markdown-based Memory Bank system for project context.
*   Ensuring consistent path management across the project.
*   Ensuring consistent application of the expert data scientist persona.
*   **Network Graph Structure:** The graph will be multi-level, containing nodes for both individual accounts and the banks they belong to, providing a richer view of transaction flows.
*   **Reminder for IV Analysis:** Investigate 2815 `CONFIRMED_FRAUD` accounts with zero PESONET/INSTAPAY transactions during IV analysis to understand their fraud patterns.
*   **WoE and IV calculation for categorical features will use the `iv_calculation.py` script.**
*   **Numerical features will be binned using user-provided specific definitions before IV calculation.**
*   **Decision to pre-process numerical binning rules for optimization.**
*   **Modeling Preprocessing Strategy:** To prevent data leakage, preprocessing steps like one-hot encoding and standardization will be fitted *only* on the training data and then applied to transform the validation and holdout sets.**
*   **Makefile Automation Strategy:** Decided to defer the update of the `Makefile` to automate the full data pipeline. This will be handled as a final project step to avoid rework while the analysis notebooks are still being finalized.
*   **Network Analysis Data Source:** The data for the network analysis will be sourced from `bank-fraud-detection-project/data_network/raw/df_network.csv`, which contains `Source Bank Name` and `Destination Bank Name`.
