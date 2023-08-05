import sys
from .nbfinder import NotebookFinder

sys.meta_path.append(NotebookFinder())
