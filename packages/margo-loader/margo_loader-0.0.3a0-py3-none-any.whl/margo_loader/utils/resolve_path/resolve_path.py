import os


def resolve_multiple_extensions(fullname, *, path=None, extensions=["nbpy", "ipynb"]):
    for ext in extensions:
        resolved = resolve_path(fullname, path=path, ext=ext)
        if resolved is not None:
            return resolved


def resolve_path(fullname, *, path=None, ext="nbpy"):
    """
    Resolve the path to a file with a given extension
    """

    # The right-most component of the dot path
    # such as foo.bar => bar
    leaf_name = fullname.rsplit(".", 1)[-1]
    if not path:
        path = [""]

    # for each path element, try to find a file
    # named {element}/{leaf_name}.{ext}. return
    # the first hit.
    for try_dir in path:
        fname = f"{leaf_name}.{ext}"
        try_path = os.path.join(try_dir, fname)

        if os.path.exists(try_path):
            return try_path

        # See if there's a version with spaces
        # instead of _s, allowing import Module_Name
        # to resolve to 'Module Name.{ext}'
        try_path = os.path.join(try_dir, fname.replace("_", " "))
        if os.path.exists(try_path):
            return try_path
