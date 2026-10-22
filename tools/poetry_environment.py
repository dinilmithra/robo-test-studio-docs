"""Pinned Poetry tooling and project environment ownership for setup entry points.

This tooling module is copied beside each standalone project's setup tools.
Only the temporary Poetry bootstrap and Poetry itself use pip; project packages
are installed by Poetry. Existing project environments are never deleted.
"""
from contextlib import contextmanager
from pathlib import Path
import os
import shutil
import subprocess
import sys
import tempfile
import venv

POETRY_VERSION = '2.5.1'


def python_in(directory):
    return Path(directory) / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')


def run(command, project, env, *, capture=False):
    print('> ' + subprocess.list2cmdline([str(x) for x in command]), flush=True)
    return subprocess.run(command, cwd=project, env=env, check=True,
                          text=True, capture_output=capture)


def clean_environment():
    env = os.environ.copy()
    for name in ('VIRTUAL_ENV','CONDA_PREFIX','CONDA_DEFAULT_ENV','PYTHONHOME'):
        env.pop(name, None)
    return env


def _poetry_python(target):
    candidates = [python_in(target), Path(sys.executable)]
    executable = shutil.which('poetry')
    if executable:
        folder = Path(executable).resolve().parent
        candidates.extend([folder/('python.exe' if os.name == 'nt' else 'python'),
                           folder/('python.exe' if os.name == 'nt' else 'python3')])
    candidates.append(Path(getattr(sys, '_base_executable', sys.executable)))
    seen = set()
    for candidate in candidates:
        if not candidate.is_file() or str(candidate) in seen:
            continue
        seen.add(str(candidate))
        result = subprocess.run([str(candidate), '-m', 'poetry', '--version'],
                                env=clean_environment(), capture_output=True, text=True,
                                check=False)
        if result.returncode == 0 and f'Poetry (version {POETRY_VERSION})' in result.stdout:
            return candidate
    return None


@contextmanager
def managed_environment(project, directory='.venv', *, bootstrap=True, timeout=30):
    """Select/create one Poetry-owned environment and reject foreign targets.

    Custom directory names use Poetry 2.5.1's environment builder;
    ordinary projects use the public `poetry env use` command. Poetry then owns
    every dependency operation in the selected environment.
    """
    project = Path(project).resolve()
    target = project/directory
    python = python_in(target)
    if target.exists() and (not python.is_file() or not (target/'pyvenv.cfg').is_file()):
        raise RuntimeError(f'Incomplete environment: {target}. Repair it before setup.')
    tool_python = _poetry_python(target)
    temporary = None
    try:
        if tool_python is None:
            if not bootstrap:
                raise RuntimeError(f'Poetry {POETRY_VERSION} is required. Run the project setup script first.')
            temporary = tempfile.TemporaryDirectory(prefix='robo-poetry-bootstrap-')
            tool_root = Path(temporary.name)/'tool'
            # This environment hosts the bootstrap tool, never application packages.
            venv.EnvBuilder(with_pip=True).create(tool_root)
            tool_python = python_in(tool_root)
            run([str(tool_python),'-m','pip','install','--disable-pip-version-check',
                 '--no-input','--retries','1','--timeout',str(timeout),
                 f'poetry=={POETRY_VERSION}'],project,clean_environment())
        command = [str(tool_python),'-m','poetry','--no-interaction']
        env = clean_environment()
        env['POETRY_VIRTUALENVS_CREATE'] = 'true'
        env['POETRY_VIRTUALENVS_IN_PROJECT'] = 'true'
        env['POETRY_VIRTUALENVS_OPTIONS_NO_PIP'] = 'false'
        if directory == '.venv':
            chosen = python if python.exists() else Path(getattr(sys,'_base_executable',sys.executable))
            run([*command,'env','use',str(chosen)],project,env)
        elif not target.exists():
            builder = ('from pathlib import Path; import sys; '
                       'from poetry.utils.env import EnvManager; '
                       'EnvManager.build_venv(Path(sys.argv[1]), '
                       'executable=Path(sys.argv[2]), with_pip=True)')
            run([str(tool_python),'-c',builder,str(target),
                 str(getattr(sys,'_base_executable',sys.executable))],project,env)
        if not python.is_file():
            raise RuntimeError(f'Poetry did not create the expected interpreter: {python}')
        run([str(python),'-c',
             "import sys; assert sys.version_info[:2] == (3,12), 'Project environment requires Python 3.12'"],project,env)
        env['VIRTUAL_ENV'] = str(target)
        env['PATH'] = str(python.parent)+os.pathsep+env.get('PATH','')
        env['POETRY_VIRTUALENVS_CREATE'] = 'false'
        env['POETRY_VIRTUALENVS_IN_PROJECT'] = 'true' if directory == '.venv' else 'false'
        selected = run([*command,'env','info','--path'],project,env,capture=True).stdout.strip()
        if Path(selected).resolve() != target.resolve():
            raise RuntimeError(f'Poetry selected {selected!r}; expected {target}. No packages were installed.')
        yield python, command, env
    finally:
        if temporary is not None:
            temporary.cleanup()


def retain_poetry_tool(python, project, env):
    """Retain only the pinned release tool in the project publishing environment."""
    run([str(python),'-m','ensurepip','--upgrade'],project,env)
    run([str(python),'-m','pip','install','--disable-pip-version-check','--no-input',
         f'poetry=={POETRY_VERSION}'],project,env)
    run([str(python),'-m','poetry','--version'],project,env)
