from argparse import ArgumentParser
from os import stat
from nbformat import read
from margo_parser.api import (
    MargoMarkdownCellPreambleBlock,
    MargoPythonCellPreambleBlock,
    MargoAssignment,
)


def register(subparsers: ArgumentParser):
    parser = subparsers.add_parser("makefile", help="generate Makefile from notebook")

    parser.add_argument("-i", "--input", metavar="NOTEBOOK_FILE", required="true")


def main(args):

    try:
        nb = read(args.input, as_version=4)
    except Exception as e:
        raise (
            f"Makefile subcommand: Could not read notebook file: '{args.input}': " + e
        )

    notebook_file = args.input
    command = f"jupyter nbconvert --to notebook --execute {notebook_file}"
    input_files = []
    output_files = []

    def add_item(lst, value):
        if type(value) == str:
            lst.append(str)
        if type(value) == list:
            lst += value

    for c in nb.cells:
        if c["cell_type"] == "markdown":
            block = MargoMarkdownCellPreambleBlock(c["source"])
        elif c["cell_type"] == "code":
            block = MargoPythonCellPreambleBlock(c["source"])

        for statement in block.statements:
            if isinstance(statement, MargoAssignment):
                if statement.name == "interface.input":
                    add_item(input_files, statement.value)

                elif statement.name == "interface.output":
                    add_item(output_files, statement.value)

    def file_list(files):
        return " ".join(files)

    def generate_rule(output_file, force_rebuild=False):
        rule = f"{output_file}: {file_list(input_files)}\n"

        first_file = output_files[0]

        # force rebuild
        # approach described here: https://www.gnu.org/software/automake/manual/html_node/Multiple-Outputs.html
        rebuild = "## Recover from the removal of $@\n"
        rebuild += f"\t@test -f $@ || rm -f {first_file}\n"
        rebuild += f"\t@test -f $@ || $(MAKE) $(AM_MAKEFLAGS) {first_file}\n"

        if force_rebuild:
            rule += rebuild
        else:
            rule += f"\t{command}\n"

        rule += "\n"

        return rule

    makefile = ""
    for idx in list(range(len(output_files))):
        makefile += generate_rule(output_files[idx], idx > 0)

    print(makefile)
