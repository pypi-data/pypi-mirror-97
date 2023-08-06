"""
This module build the app via pyinstaller.
It help to build applications build with eel.

There is one main function `build_app`. Check it's help for how to use
it (should be very simple).

Note:
    Build pyinstaller on your pc, otherwise antivirus can check the file for a while on first run.
    Download from github, cd to bootloader and

    ```
    python ./waf all
    ```

    Back to pyinstaller folder and python `setup.py`
"""

import subprocess
import shutil
from pathlib import Path
from mypythontools import misc
import mylogging


def build_app(
        main_file='app.py', preset=None,
        root_path=None, web_path=None,
        build_web=None, remove_last_build=False,
        console=True, debug=False, icon=False, hidden_imports=[],
        ignored_packages=[], datas=[], name=None, env_vars={},
        cleanit=True):
    """One script to build .exe app from source code. it use pyinstaller, which must be localy installed.
    Build pyinstaller bootloader manually to avoid antivirus problems.
    This script automatically generate .spec file, build node web files and add environment variables during build.

    This script suppose some structure of the app. You can use python app starter on the same repository.

    You can use presets (or create your own.) - then you don't need to set other except the main_file.

    Args:
        main_file (str, optional): Main file path or name with extension. Main file is found automatically
            and don't have to be in root. Defaults to 'app.py'.
        root_path ((Path, str), optional): Root where build and dist folders are (as well as docs, travis.yaml are). If None,
            cwd (current working directory) infered. Defaults to None.
        web_path ((Path, str), optional): Folder with index.html. Defaults to None.
        preset (str, optional): Edit other params for specific use cases (append to hidden_imports, datas etc.)
            Options ['eel'].
        build_web (bool, optional): If application contain package.json in folder 'gui', build it (if using eel). Defaults to None.
        remove_last_build (bool, optional): If some problems, it is possible to delete build and dist folders. Defaults to False.
        console (bool, optional): Before app run terminal window appears (good for debugging). Defaults to False.
        debug (bool, optional): If no console, then dialog window with traceback appears. Defaults to False.
        icon ((Path, str), optional): Path or name with extension to .ico file (!no png!). Defaults to None.
        hidden_imports (list, optional): If app is not working, it can be because some library was not builded. Add such
            libraries into this list. Defaults to [].
        ignored_packages (list, optional): Libraries take space even if not necessary. Defaults to [].
        datas (list, optional): Add static files to build. Example: [('my_source_path, 'destination_path')].
        env_vars (dict, optional): Add some env vars during build. Mostly to tell main script that it's production (ne development) mode. Defaults to {}.
        name (str, optional): If name of app is different than main py file. Defaults to None.
        cleanit (bool, optional): Remove spec file and var env py hook. Defaults to True.
    """

    # Try to recognize the structure of app
    root_path = root_path if root_path else misc.root_path

    build_path = root_path / 'build'

    if not build_path.exists():
        build_path.mkdir(parents=True, exist_ok=True)

    # Remove last dist manually to avoid permission error if opened in some application
    dist_path = root_path / 'dist'

    if dist_path.exists():
        try:
            shutil.rmtree(dist_path, ignore_errors=False)
        except (PermissionError, OSError):
            raise PermissionError(mylogging.return_str("App is opened (May be in another app(terminal, explorer...)). Close it first."))

    # May be just name - not absolute
    main_file_path = Path(main_file)

    if not main_file_path.exists():

        # Iter paths and find the one
        main_file_path = misc.find_path(main_file_path, exclude=['node_modules', 'build'])

        if not main_file_path.exists():
            raise KeyError("Main file not found, not infered and must be configured in params...")

    main_file_path = main_file_path.resolve()

    if not name:
        name = main_file_path.stem

    main_folder_path = main_file_path.parent

    if icon:
        icon_path = Path(icon)

        if not icon_path.exists():

            # Iter paths and find the one
            icon_path = misc.find_path(icon_path, exclude=['node_modules', 'build'])

            if not icon_path.exists():
                raise KeyError("Icon not found, not infered check path or name...")
    else:
        icon_path = None

    if preset == 'eel':
        if not web_path:
            web_path = misc.find_path('index.html', exclude=['public', 'node_modules', 'build']).parent

        else:
            web_path = Path(web_path)

        if not web_path.exists():
            raise KeyError("Build web assets not found, not infered and must be configured in params...")

        if build_web is None:
            build_web = True

        hidden_imports = [*hidden_imports, 'bottle_websocket']

        datas = tuple([*datas, (web_path.as_posix(), 'gui')])
        env_vars = {**env_vars, 'MY_PYTHON_VUE_ENVIRONMENT': 'production'}

    generated_warning = """
#########################
### File is generated ###
#########################

# Do not edit this file, edit build_script"""

    if env_vars:
        env_vars_template = f"""
{generated_warning}

import os
for i, j in {env_vars}.items():
    os.environ[i] = j
"""

        env_path = (build_path / 'env_vars.py')

        with open(env_path, 'w') as env_vars_py:
            env_vars_py.write(env_vars_template)
        runtime_hooks = [env_path.as_posix()]
    else:
        runtime_hooks = None

    spec_template = f"""
{generated_warning}

import sys
from pathlib import Path
import os

sys.setrecursionlimit(5000)
block_cipher = None

a = Analysis(['{main_file_path.as_posix()}'],
            pathex=['{main_folder_path.as_posix()}'],
            binaries=[],
            datas={datas},
            hiddenimports={hidden_imports},
            hookspath=[],
            runtime_hooks={runtime_hooks},
            excludes={ignored_packages},
            win_no_prefer_redirects=False,
            win_private_assemblies=False,
            cipher=block_cipher,
            noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
            cipher=block_cipher)
exe = EXE(pyz,
        a.scripts,
        [],
        exclude_binaries=True,
        name='{name}',
        debug={debug},
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        console={console},
        icon={f"'{icon_path.as_posix()}'" if icon else None})
coll = COLLECT(exe,
            a.binaries,
            a.zipfiles,
            a.datas,
            strip=False,
            upx=True,
            upx_exclude=[],
            name='{name}')
"""

    spec_path = build_path / 'app.spec'

    with open(spec_path, 'w') as spec_file:
        spec_file.write(spec_template)

    if remove_last_build:
        try:
            shutil.rmtree('build', ignore_errors=True)
        except Exception:
            pass

    # Build JS to static asset
    if build_web:
        gui_path = misc.find_path('package.json').parent
        subprocess.run(['npm', 'run', 'build'], shell=True, check=True, cwd=gui_path)

    # Build py to exe

    subprocess.run(['pyinstaller', '-y', spec_path.as_posix()], shell=True, check=True, cwd=root_path)

    if cleanit:
        try:
            spec_path.unlink()
            env_path.unlink()
        except Exception:
            pass
