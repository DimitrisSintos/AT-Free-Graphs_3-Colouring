# AT-Free Graphs 3-Colouring

## Installation

1. Install `python3.10-venv` using `apt`:

    ```bash
    sudo apt install python3.10-venv
    ```

2. Create a Python virtual environment:

    ```bash
    python -m venv .venv --prompt AT-free-3-colouring
    ```

3. Activate the virtual environment:

    ```bash
    source .venv/bin/activate
    ```

4. Install the required dependencies from `requirements.txt`:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the program using Python 3. You can optionally provide an input graph file (check input-graph.json for an example):

```bash
python3 main.py <optional-input-graph.json>
