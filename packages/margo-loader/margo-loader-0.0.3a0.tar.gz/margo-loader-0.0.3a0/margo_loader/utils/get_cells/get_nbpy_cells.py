from .FakeCell import FakeCell


def get_nbpy_cells_recursively(source_lines, cell_list=[]):

    if len(source_lines) < 1:
        return cell_list

    cell = FakeCell()

    line_index = 0
    while line_index < len(source_lines):
        line = source_lines[line_index]

        if line.strip().startswith("# %%") or line.strip().startswith("#%%"):
            break

        cell.append_source(line + "\n")
        line_index += 1

    if (line_index + 1) < len(source_lines):
        remaining_lines = source_lines[line_index + 1 :]
    else:
        remaining_lines = []

    return get_nbpy_cells_recursively(remaining_lines, cell_list + [cell])


def get_cells(path):

    """
    Generate a cells array from a python file using vscode code cells
    """
    source = open(path).read()
    lines = source.splitlines()

    return get_nbpy_cells_recursively(lines)
