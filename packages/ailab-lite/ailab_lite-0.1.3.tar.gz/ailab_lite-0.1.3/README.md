ailab-lite
===============================

Jupyter Notebook extension GUI node editor

Installation
------------

To install use pip:

    $ pip install ailab_lite

For a development installation (requires [Node.js](https://nodejs.org) and [Yarn version 1](https://classic.yarnpkg.com/)),

    $ git clone https://github.com/fathoms-io/ailab-lite.git
    $ cd ailab-lite
    $ pip install -e .
    $ jupyter nbextension install --py --symlink --overwrite --sys-prefix ailab_lite
    $ jupyter nbextension enable --py --sys-prefix ailab_lite

When actively developing your extension for JupyterLab, run the command:

    $ jupyter labextension develop --overwrite ailab_lite

Then you need to rebuild the JS when you make a code change:

    $ cd js
    $ yarn run build

You then need to refresh the JupyterLab page when your javascript changes.

### Usage:

#### Notebook:
Import node editor widget:
```python
from ailab_lite import NodeEditorWidget
```

Import pandas:
```python
import pandas as pd
```

Decalare dataset:
```python
example = pd.read_csv("example.csv")
```

Run widget:
```python
NodeEditorWidget(env=globals())
```