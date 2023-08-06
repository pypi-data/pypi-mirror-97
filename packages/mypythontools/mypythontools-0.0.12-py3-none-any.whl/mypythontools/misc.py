"""
Only internal helping module for other modules. Not supposed to be used by users.
"""
from pathlib import Path
import sys
import mylogging


# Root is usually current working directory, if not, use `set_root` function.
root_path = Path.cwd()


def set_root(set_root_path=None):
    """Root folder is inferred automatically if call is from git_hooks folder or from root (cwd).
    If more projects opened in IDE, root project path can be configured here.

    Args:
        root_path ((str, pathlib.Path)): Path to project root.
    """
    if set_root_path:
        root_path = Path(set_root_path)

    if not root_path.as_posix() in sys.path:
        sys.path.insert(0, root_path.as_posix())


def find_path(file, folder=None, exclude=['node_modules', 'build', 'dist'], levels=4):
    """Look on files in folder (cwd() by default) and find file with it's folder.

    Args:
        file (str): Name with extension e.g. "app.py".
        folder (str): Name with extension e.g.. If None, then cwd is used. Defaults to None.
        exclude (str): List of folder names (anywhere in path) that will be ignored. Defaults to ['node_modules', 'build', 'dist'].
        levels (str): Recursive number of analyzed folders. Defaults to 4.

    Returns:
        Path: Path of file.

    Raises:
        FileNotFoundError: If file is not found.
    """

    folder = root_path if not folder else Path(folder).resolve()

    for lev in range(levels):
        glob_file_str = f"{'*/' * lev}{file}"

        for i in folder.glob(glob_file_str):
            isthatfile = True
            for j in exclude:
                if j in i.parts:
                    isthatfile = False
                    break
            if isthatfile:
                return i

    # If not returned - not found
    raise FileNotFoundError(mylogging.return_str(f'File `{file}` not found'))
