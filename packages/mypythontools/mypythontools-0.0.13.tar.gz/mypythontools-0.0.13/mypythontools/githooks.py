"""
This module is to be used in githooks (some code automatically executed before commit for example).

How to
------

Create folder git_hooks with git hook file - for prec commit name must be `pre-commit` (with no extension)
Hooks in git folder are gitignored by default (and hooks is not visible on first sight).

Then add hook to git settings - run in terminal (last arg is path (created folder))

```shell
git config core.hooksPath git_hooks
```

In created folder on first two lines copy this

```python
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
```

Then just import any function from here and call with desired params. E.g.

Examples:
    >>> mypythontools.githooks.run_tests()
    >>> mypythontools.githooks.generate_readme_from_init('mylibrary')
    >>> mypythontools.githooks.sphinx_docs_regenerate('mylibrary')

That will generate readme from __init__.py and call sphinx-apidoc and create rst files ind doc source folder.
"""

import subprocess
import inspect
from pathlib import Path
import importlib

from . import misc


def run_tests(test_path=None):
    import pytest
    """Run tests and if not passing, raise an error.

    Args:
        test_path ((str, pathlib.Path)), optional): Usually autodetected (if cwd / tests). Defaults to None.

    Raises:
        Exception: If any test fail, it will raise exception (git hook do not continue...).
    """

    if not test_path:
        test_path = misc.root_path / 'tests'

    pytested = pytest.main(["-x", test_path.as_posix()])

    if pytested == 1:
        raise Exception("Pytest failed")


def sphinx_docs_regenerate(project_name, root_path=None, app_path=None, docs_path=None, build_locally=0, git_add=True):
    """This will generate all rst files necessary for sphinx documentation generation.
    It automatically delete removed and renamed files.

    Function suppose sphinx build and source in separate folders...

    Args:
        root_path ((str, Path), optional): Where docs folder is. Usually infered automatically. Defaults to None.
        app_path ((str, Path), optional): Where application scripts are. Usually infered automatically. Defaults to None.
        docs_path ((str, Path), optional): Where source folder is. Usually infered automatically. Defaults to None.
        project_name (str): Name of your project (used in sphinx-apidoc).
        build_locally (bool, optional): If true, build build folder with html files locally. Defaults to 0.
        git_add (bool, optional): Whether to add generated files to stage. False mostly for testing reasons.
    Note:
        Function suppose structure of docs like

        -- docs
        -- -- source
        -- -- -- conf.py
        -- -- make.bat

        If you are issuing error, try set project root path with `set_root`
    """

    if not importlib.util.find_spec('sphinx'):
        raise ImportError("Sphinx library is necessary for docs generation. Install via `pip install sphinx`")

    if not root_path:
        root_path = misc.root_path
    if not docs_path:
        docs_path = root_path / 'docs'

    docs_source_path = root_path / 'docs' / 'source'

    if not app_path:
        app_path = root_path / project_name

    for p in Path(docs_source_path).iterdir():
        if p.name not in ['conf.py', 'index.rst', '_static', '_templates']:
            p.unlink()

    if build_locally:
        subprocess.run(['make', 'html'], shell=True, cwd=docs_path, check=True)

    subprocess.run(['sphinx-apidoc', '-f', '-e', '-o', 'source', app_path.as_posix()], shell=True, cwd=docs_path, check=True)

    if git_add:
        subprocess.run(['git', 'add', 'docs'], shell=True, cwd=root_path, check=True)


def generate_readme_from_init(project_name, git_add=True):
    """Because i had very similar things in main __init__.py and in readme. It was to maintain news in code.
    For better simplicity i prefer write docs once and then generate. One code, two use cases.

    Why __init__? - Because in IDE on mouseover developers can see help.
    Why README.md? - Good for github.com

    Args:
        project_name (str): Module name (module must be imported).
        git_add (bool, optional): Whether to add generated files to stage. False mostly for testing reasons.
    """

    ## Generate README.md from __init__.py
    my_module = importlib.import_module(project_name)
    docstrings = inspect.getdoc(my_module)

    root_path = misc.root_path

    with open(root_path / 'README.md', 'w') as file:
        file.write(docstrings)

    if git_add:
        subprocess.run(['git', 'add', 'README.md'], shell=True, cwd=root_path, check=True)
