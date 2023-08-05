"""
Get the cells of a notebook document.
"""

from . import get_nbpy_cells
from . import get_ipynb_cells

CELL_RESOLVERS = {"ipynb": get_ipynb_cells, "nbpy": get_nbpy_cells}


def infer_type(path, extensions=["ipynb", "nbpy"]):
    for ext in extensions:
        if path.lower().endswith(f".{ext}"):
            return ext


def get_cells(path, notebook_type=None):
    if notebook_type is None:
        notebook_type = infer_type(path)
    if notebook_type is None or notebook_type not in CELL_RESOLVERS:
        raise Exception("Unsupported file name: " + path)

    cell_resolver = CELL_RESOLVERS[notebook_type]
    return cell_resolver.get_cells(path)
