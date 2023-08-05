"""Process a notebook with margo preamble"""
from margo_parser.api import (
    MargoBlock,
    MargoMarkdownCellPreambleBlock,
    MargoPythonCellPreambleBlock,
    MargoStatementTypes,
    MargoDirective,
)
import json
import re
import sys
import types


def remove_magics(source: str) -> str:
    """Remove magics from source for execution outside of Jupyter"""

    ret = ""
    for line in source.splitlines():
        if line.strip().startswith("%"):
            continue
        ret += line + "\n"
    return ret


def get_views(cell_preamble: MargoBlock):
    """Get the submodules this cell belongs to"""
    ret = []
    for statement in cell_preamble.statements:
        if statement.type != MargoStatementTypes.DECLARATION:
            continue
        if statement.name != "submodule":
            continue
        ret = ret + statement.value

    return ret


def preamble_contains_directive(cell_preamble: MargoBlock, directive_list):
    for statement in cell_preamble.statements:
        if (
            statement.type == MargoStatementTypes.DIRECTIVE
            and statement.name in directive_list
        ):
            return True
    return False


def preamble_contains_ignore_cell(cell_preamble: MargoBlock):
    """Determine if a cell contains ignore-cell margo directive"""

    return preamble_contains_directive(cell_preamble, ["ignore-cell", "skip"])


def preamble_contains_stop_module(cell_preamble: MargoBlock):
    """Determine if a cell contains a stop-module subcommand"""

    return preamble_contains_directive(cell_preamble, ["stop-module", "stop"])


def preamble_contains_start_module(cell_preamble: MargoBlock):
    """Determine if a cell contains a start-module subcommand"""
    return preamble_contains_directive(
        cell_preamble,
        [
            "start-module",
            "start",
        ],
    )


def preamble_contains_not_a_module(cell_preamble: MargoBlock):
    """Determine if a notebook declares that it is not to be imported
    by using the 'not-a-module' directive"""

    return preamble_contains_directive(cell_preamble, ["not-a-module", "do-not-import"])


def get_preamble(cell):
    if cell.cell_type == "markdown":
        cell_preamble = MargoMarkdownCellPreambleBlock(cell.source)
    else:
        cell_preamble = MargoPythonCellPreambleBlock(cell.source)

    return {"cell": cell, "preamble": cell_preamble}


class Processor:
    def __init__(self, module, name):
        self.module = module
        self.name = name

    def process_cells(self, cells):
        """Parse preambles and execute code cells of a notebook accordingly
        Currently supports:
        # :: ignore-cell :: to skip this cell
        # :: submodule: 'submodule_name' :: to create a virtual submodule in
        which this cell's code will be executed and can later be imported with
        from notebook.submodule_name import stuff_you_defined

        If first cell is markdown, it will be used as the module's docstring
        """
        idx = -1
        exec_enabled = True

        margo_cells = [get_preamble(c) for c in cells]
        for margo_cell in margo_cells:
            if preamble_contains_not_a_module(margo_cell["preamble"]):
                raise Exception(
                    "Cannot import: This notebook declares that it is not a module."
                )

        def exec_wrapper(code, context):
            if not exec_enabled:
                return
            exec(code, context)

        for margo_cell in margo_cells:
            idx += 1
            cell = margo_cell["cell"]
            cell_preamble = margo_cell["preamble"]
            # If the first cell is a markdown cell, use it
            # as the module docstring
            if idx == 0 and cell.cell_type == "markdown":
                self.module.__doc__ = cell.source

            # cell_preamble = get_preamble_block(cell.source, cell_type=cell.cell_type)
            # if cell.cell_type == "markdown":
            #     cell_preamble = MargoMarkdownCellPreambleBlock(cell.source)
            # else:
            #     cell_preamble = MargoPythonCellPreambleBlock(cell.source)

            cell_source = remove_magics(cell.source)

            # ignore-cell support
            if preamble_contains_ignore_cell(cell_preamble):
                continue

            # stop-module support
            if preamble_contains_stop_module(cell_preamble):
                exec_enabled = False

            # start-module support
            if preamble_contains_start_module(cell_preamble):
                exec_enabled = True

            # view: module.view_name support ::
            views = get_views(cell_preamble)
            for view in views:
                full_view_name = self.name + "." + view

                if full_view_name in sys.modules:
                    mod = sys.modules[full_view_name]

                else:
                    mod = types.ModuleType(full_view_name)
                    sys.modules[full_view_name] = mod
                # Execute the code code within the given view name
                exec_wrapper(cell_source, mod.__dict__)
                # TODO - This version does not do it, but I should
                # probably execute every cell in a view. Cells
                # without a view specified should run in a default
                # view, and then that view should be assigned to the main
                # module at the end
                self.module.__dict__[view] = mod

            if cell.cell_type == "code":
                exec_wrapper(cell_source, self.module.__dict__)
