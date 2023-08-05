import os
from importlib.machinery import ModuleSpec

# from .find_notebook import find_notebook
from .utils.resolve_path import resolve_multiple_extensions
from .nbloader import NotebookLoader


class NotebookFinder(object):
    """Module finder that locates Jupyter Notebooks"""

    def __init__(self):
        self.loaders = {}

    # TODO - Make use of the target: https://www.python.org/dev/peps/pep-0451/#the-target-parameter-of-find-spec
    def find_spec(self, name, path, target=None):
        # if not (find_notebook(name, path)):
        #     return None
        resolved = resolve_multiple_extensions(name, path=path)
        if resolved is None:
            return

        return ModuleSpec(name, self.find_module(name, path))

    def find_module(self, fullname, path=None):
        # This is deprecated, but keeping it should allow this to work
        # with python < 3.4. However, this legacy support is not a goal

        nb_path = resolve_multiple_extensions(fullname, path=path)
        if not nb_path:
            return

        key = path
        if path:
            # lists aren't hashable
            key = os.path.sep.join(path)

        if key not in self.loaders:
            self.loaders[key] = NotebookLoader(path)
        return self.loaders[key]
