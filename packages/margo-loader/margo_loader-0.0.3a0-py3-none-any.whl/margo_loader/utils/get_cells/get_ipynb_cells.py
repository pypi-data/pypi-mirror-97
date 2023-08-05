import io
from nbformat import read


def get_cells(path):
    with io.open(path, "r", encoding="utf-8") as f:
        cells = read(f, 4).cells

    return cells
