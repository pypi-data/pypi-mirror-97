# nb_as_module

`pip install nb_as_module`

Load a Jupyter Notebook as a module object.

E.g.

```python
from nb_as_module import nb_as_module

my_module = nb_as_module('path/to/notebook.ipynb', name='my_module)

my_module.hello()  # where `hello` is a function defined in the notebook.
```

Put \<!--docstring--> at the beggining of markdown cells,
to use them as `__doc__` documentation.
