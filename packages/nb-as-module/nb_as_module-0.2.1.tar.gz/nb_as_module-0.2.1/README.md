# nb_as_module

[![](https://github.com/sradc/nb_as_module/workflows/Python%20package/badge.svg)](https://github.com/sradc/nb_as_module/commits/)

`pip install nb_as_module`

Load a Jupyter Notebook as a module object.

### Examples

```python
from nb_as_module import nb_as_module

my_module = nb_as_module('path/to/notebook.ipynb', name='my_module')

my_module.hello()  # where `hello` is a function defined in the notebook.
```

There is also a helper module for Google Colab.

```python
import nb_as_module.colab

# Mount Google Drive, where Colab notebooks are saved.
# (Note you will be asked permission for access here.)
nb_as_module.colab.mount_drive()

# Get a list of your notebooks:
list_of_notebooks = nb_as_module.colab.list_nbs()
print(list_of_notebooks)
#> ['hello.ipynb', ...]

# Load one of the notebooks in the list, as a module:
hello = as_module('hello.ipynb', 'hello')

# Run a function from the module.
hello.hello()
#> Hello, world.
```

### __doc__

Put \<!--docstring--> at the beggining of markdown cells,
to use them as `__doc__` documentation. (If multiple cells are used,
they will be concatenated.)
