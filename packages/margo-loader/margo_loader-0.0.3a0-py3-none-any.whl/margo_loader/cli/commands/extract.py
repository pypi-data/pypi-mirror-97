from argparse import ArgumentParser
from nbformat import read
from margo_parser.api import (
    MargoMarkdownCellPreambleBlock,
    MargoPythonCellPreambleBlock,
    MargoStatementTypes,
)
import json


def register(subparsers: ArgumentParser):
    parser = subparsers.add_parser("extract", help="extract variables from notebook")

    parser.add_argument("-i", "--input", metavar="NOTEBOOK_FILE", required="true")
    parser.add_argument(
        "-f", "--format", metavar="DECLARATION_FORMAT", choices=["json", "yaml", "raw"]
    )
    parser.add_argument(
        "-p", "--property", metavar="PROPERTY", help="The property to extract"
    )


def main(args):

    try:
        nb = read(args.input, as_version=4)
    except Exception as e:
        raise (
            f"Extract subcommand: Could not read notebook file: '{args.input}': " + e
        )

    declarations = {}

    def add_to_declaration(name, val):
        if args.format == "raw":
            val = str(val)
        else:
            val = [val]

        if name not in declarations:
            declarations[name] = val
            return
        else:
            declarations[name] += val

    for c in nb.cells:
        if c["cell_type"] == "markdown":
            block = MargoMarkdownCellPreambleBlock(c["source"])
        elif c["cell_type"] == "code":
            block = MargoPythonCellPreambleBlock(c["source"])
        else:
            continue
        for statement in block.statements:
            if statement.type != MargoStatementTypes.DECLARATION:
                continue
            add_to_declaration(statement.name, statement.value)

    def print_report():
        if args.property and args.property not in declarations:
            return
        elif args.property and args.format == "raw":
            print(declarations[args.property])
        elif args.property:
            print(json.dumps(declarations[args.property], indent=2))
        else:
            print(json.dumps(declarations, indent=2))

    print_report()
