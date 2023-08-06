mypythontools
=============

Some tools/functions/snippets used across projects.

Usually used from IDE. Root path is infered and things like docs generation on pre-commit
githook, building application with pyinstaller or deploying to Pypi is matter of calling one function.

Many projects - one codebase.

If you are not sure whether structure of app that will work with this code, there is python starter repo
on `https://github.com/Malachov/my-python-starter`

Modules:
--------

build
-----
Build your app with pyinstaller just with calling one function `build_app`.
Check function doctrings for how to do it.

See module help for more informations.

githooks
--------

Some functions runned every each git action (usually before commit).

Can derive run pytest tests, `README.md` from `__init__.py` or generate rst files necessary for sphinx docs generator.
All with one line

Check module docstrings for how to use it.

deploy
------

Deploy app on Pypi.


pyvueel
-------
Common functions for Python / Vue / Eel project.

Run `mypythontools.pyvueel.help_starter_pack_vue_app()` for tutorial how to create such an app.


misc
----
Miscellaneous
Set up root path if not cwd for example.