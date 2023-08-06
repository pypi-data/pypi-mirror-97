import pathlib
from nb_as_module.nb_as_module import *

root_dir = pathlib.Path(__file__).parents[1]
__version__ = (root_dir / "VERSION").read_text()
