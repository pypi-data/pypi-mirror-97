import os

# This is unused legacy code based on the following example.
# I am keeping it in this repo for testing purposes for a little while


def find_notebook(fullname, path=None):
    """find a notebook, given its fully qualified name and an optional path

    This turns "foo.bar" into "foo/bar.ipynb"
    and tries turning "Foo_Bar" into "Foo Bar" if Foo_Bar
    does not exist.
    """
    name = fullname.rsplit(".", 1)[-1]
    if not path:
        path = [""]
    for d in path:
        nb_path = os.path.join(d, name + ".ipynb")
        if os.path.isfile(nb_path):
            return nb_path
        # let import Notebook_Name find "Notebook Name.ipynb"
        nb_path = nb_path.replace("_", " ")
        if os.path.isfile(nb_path):
            return nb_path

        # load .nbpy documents
        nbpy_path = os.path.join(d, name + ".nbpy")
        if os.path.isfile(nbpy_path):
            return nbpy_path
