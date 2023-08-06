"""
Allow to deploy project.
Possible destinations: PYPI.
"""
import subprocess
import os
import mylogging
import shutil

from . import misc


def deploy_to_pypi(setup_path=None):
    """Publish python library to Pypi. Username and password are set
    with env vars `TWINE_USERNAME` and `TWINE_PASSWORD`.

    Args:
        setup_path((str, pathlib.Path)): Function suppose, that there is a setup.py in cwd. If not, pass path to setup.py.
        username
        password
    """
    try:
        os.environ['TWINE_USERNAME']
        os.environ['TWINE_PASSWORD']
    except KeyError:
        raise KeyError(mylogging.return_str('Setup env vars TWINE_USERNAME and TWINE_PASSWORD to use deploy.'))

    setup_path = misc.root_path if not setup_path else setup_path

    setup_py_path = setup_path / 'setup.py'

    if not setup_py_path.exists():
        setup_py_path = misc.find_path('setup.py', exclude=['node_modules'])
        setup_path = setup_py_path.parent

        if not (setup_path / 'setup.py').exists():
            raise FileNotFoundError(mylogging.return_str("Setup.py file not found. Setup `setup_path` param."))

    subprocess.run(['python', 'setup.py', 'sdist', 'bdist_wheel'], cwd=setup_path, shell=True, check=True)

    subprocess.run(['twine', 'upload', '-u', os.environ['TWINE_USERNAME'], '-p', os.environ['TWINE_PASSWORD'], 'dist/*'], cwd=setup_path, shell=True, check=True)

    shutil.rmtree(root_path / 'tests' / 'build')
    shutil.rmtree(root_path / 'tests' / 'dist')
