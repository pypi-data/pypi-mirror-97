# BSD 3-Clause License

# Copyright (c) 2021, S Radcliffe
# Copyright (c) 2017, Project Jupyter Contributors
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.

# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.

# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
Load a Jupyter Notebook as a module object.

Partially based on:
https://github.com/jupyter/notebook/blob/57fcc413b4cd8e2c15d3fd4d14f79f3f339cfd12/docs/source/examples/Notebook/Importing%20Notebooks.ipynb
"""
import io
import pathlib
import sys
import types

import IPython
import nbformat


DOCSTRING_FLAG = "<!--docstring-->"


def nb_as_module(path, name=None):
    """Load a Jupyter Notebook as a module object.

    Args:
        path :: str
            The path to the notebook. E.g. '/home/user/my-notebook.ipynb'
        name :: str
            The name of the module. E.g. 'my_notebook'
            If name==`None` the file name is used (without the file extension).
    Returns:
        A module object, containing the methods and variables defined in the notebook.

        E.g.
        my_module = nb_as_module('path/to/notebook.ipynb')
        my_module.hello()  # where `hello` is a function defined in the notebook.

    Notes:
        Put <!--docstring--> at the beggining of markdown cells,
        to use them as `__doc__` documentation.
    """
    if not name:
        name = pathlib.Path(path).stem

    module = types.ModuleType(name)

    shell = IPython.core.interactiveshell.InteractiveShell.instance()

    # load the notebook object
    with io.open(path, "r", encoding="utf-8") as f:
        nb = nbformat.read(f, 4)

    # --- Execute notebook cells ---

    # Enable cell-magic to work:
    saved_user_ns = shell.user_ns
    shell.user_ns = module.__dict__

    try:
        with IPython.utils.io.capture_output() as captured:
            for cell in nb.cells:
                if cell.cell_type == "code":
                    code = shell.input_transformer_manager.transform_cell(cell.source)
                    exec(code, module.__dict__)
    finally:
        shell.user_ns = saved_user_ns

    # --- Find docstring cells ---
    docstring = "".join(
        [
            cell["source"].strip(DOCSTRING_FLAG).strip()
            for cell in nb.cells
            if getattr(cell, "source", "").startswith(DOCSTRING_FLAG)
        ]
    )
    module.__doc__ = docstring

    # -- Add possibly useful attributes --
    module.__file__ = path
    module.__dict__["get_ipython"] = IPython.get_ipython
    sys.modules[name] = module

    return module
