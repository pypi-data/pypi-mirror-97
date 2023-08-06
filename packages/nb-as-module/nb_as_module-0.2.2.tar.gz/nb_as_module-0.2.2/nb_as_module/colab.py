"""Helper functions, for importing Google Colab notebooks.

First use mount() to gain access to Google Drive (where Colab stores the notebooks).
Use list_nbs() to see the notebooks available.
Then use as_module(filename, modulename) where filename is a name in list_nbs().

E.g. 
import nb_as_module.colab

# Mount Google Drive, where Colab notebooks are saved.
# (Note you will be asked permission for access here.)
nb_as_module.colab.mount_drive()

# Get a list of your notebooks:
list_of_notebooks = nb_as_module.colab.list_nbs()
print(list_of_notebooks)
#> ['hello.ipynb']

# Load one of the notebooks in the list, as a module:
hello = nb_as_module.colab.as_module('hello.ipynb', 'hello')

# Run a function in the module.
hello.hello()
#> Hello, world.
"""
import pathlib
from google.colab import drive
from nb_as_module import nb_as_module


COLAB_DIR = pathlib.Path("/content/drive/MyDrive/Colab Notebooks")


def mount_drive():
    "Mount Google Drive, to access Colab notebooks."
    drive.mount("/content/drive")


def list_nbs():
    "List the Colab notebooks found in /content/drive/MyDrive/Colab Notebooks/"
    return [str(nb.relative_to(COLAB_DIR)) for nb in COLAB_DIR.rglob("*.ipynb")]


def as_module(filename, modulename=""):
    "Load a Colab notebook as a Python module."
    return nb_as_module(COLAB_DIR / filename, modulename)
