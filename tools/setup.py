"""Poetry environment setup and local documentation preview."""

# Standalone Poetry environment support (kept identical across project setup scripts).
from contextlib import contextmanager
from pathlib import Path
import os
import shutil
import subprocess
import sys
import tempfile
import venv
import re
import tomllib
import threading
import time

POETRY_VERSION = "2.5.1"

# Python security advisory, 2026-10-20. The wheel digest is part of the URL.
MINIMUM_PIP_VERSION = (26, 2, 2)
MINIMUM_CERTIFI_VERSION = (2026, 10, 19)
CERTIFI_REQUIREMENT = "certifi>=2026.10.19"
PIP_BOOTSTRAP_URL = "pip @ https://files.pythonhosted.org/packages/3f/06/3e4420302363fbb71be3c7f35ce042f54bfca330e3e66b3a2e3c4cca579f/pip-26.2.2-py3-none-any.whl#sha256=fd7f4dfa8190e014013b9f08f3e973f4e4c26ffd179a204895533a7254813a70"
PIP_BOOTSTRAP_CODE = r"""
import importlib.metadata as metadata
import re
import subprocess
import sys

def current_pip():
    try:
        value = metadata.version('pip')
    except metadata.PackageNotFoundError:
        return (0, 0, 0)
    match = re.fullmatch(r'(\d+)\.(\d+)(?:\.(\d+))?', value)
    return tuple(int(v or 0) for v in match.groups()) if match else (0, 0, 0)

if current_pip() == (0, 0, 0):
    import ensurepip
    ensurepip.bootstrap(upgrade=True)
if current_pip() < (26, 2, 2):
    subprocess.check_call([
        sys.executable, '-m', 'pip', 'install', '--upgrade', '--no-deps',
        '--no-cache-dir', '--disable-pip-version-check', '--no-input',
        '--retries', '1', '--timeout', sys.argv[2], sys.argv[1],
    ])
if current_pip() < (26, 2, 2):
    raise RuntimeError('Security bootstrap failed: pip >=26.2.2 is required.')
print('Verified secure pip: ' + metadata.version('pip'))
"""
CERTIFI_CHECK_CODE = """
from importlib.metadata import version
import re
import sys
match = re.fullmatch(r'(\\d+)\\.(\\d+)\\.(\\d+)', version('certifi'))
sys.exit(0 if match and tuple(map(int, match.groups())) >= (2026, 10, 19) else 1)
"""


def secure_pip_command(python, timeout=30):
    """Build a self-contained, checksum-verified pip bootstrap command.

    This runs inside the target interpreter, keeps newer stable pip versions,
    and uses offline ensurepip only when pip is missing.
    """
    return [
        str(python),
        "-c",
        PIP_BOOTSTRAP_CODE,
        PIP_BOOTSTRAP_URL,
        str(max(timeout, 1)),
    ]


def tool_certificates_are_secure(python):
    """Probe a Poetry tool environment without modifying its global packages."""
    try:
        return (
            subprocess.run(
                [str(python), "-c", CERTIFI_CHECK_CODE],
                env=clean_environment(),
                capture_output=True,
                text=True,
                check=False,
                timeout=10,
            ).returncode
            == 0
        )
    except (OSError, subprocess.TimeoutExpired):
        return False


def poetry_command_is_secure(command):
    """Find the interpreter of an external Poetry command and check its CA bundle."""
    if len(command) >= 3 and command[1:3] == ["-m", "poetry"]:
        candidate = Path(command[0])
    else:
        executable = Path(command[0]).resolve()
        candidate = python_in(executable.parent.parent)
    return candidate.is_file() and tool_certificates_are_secure(candidate)


def secure_locked_certifi(poetry, project, env):
    """Use Poetry to repair an unsafe locked certifi; never hand-edit lock hashes."""
    lock = Path(project) / "poetry.lock"

    def unsafe():
        if not lock.is_file():
            return False
        packages = tomllib.loads(lock.read_text(encoding="utf-8")).get("package", [])
        for package in packages:
            if package["name"] == "certifi":
                match = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)", package["version"])
                if (
                    not match
                    or tuple(map(int, match.groups())) < MINIMUM_CERTIFI_VERSION
                ):
                    return True
        return False

    if unsafe():
        run([*poetry, "update", "certifi", "--lock"], project, env)
        if unsafe():
            raise RuntimeError(
                "Poetry still locks an unsafe certifi. Allow certifi>=2026.10.19 in project constraints, then rerun setup."
            )


def python_in(directory):
    return Path(directory) / ("Scripts/python.exe" if os.name == "nt" else "bin/python")


def run(command, project, env, *, capture=False):
    tooling_install = (
        "pip" in command
        and "install" in command
        and any(str(value).startswith("poetry==") for value in command)
    )
    if command[1:3] == ["-c", PIP_BOOTSTRAP_CODE]:
        print(f"> {command[0]}: verify/upgrade secure pip", flush=True)
    else:
        print("> " + subprocess.list2cmdline([str(x) for x in command]), flush=True)
    if not tooling_install:
        return subprocess.run(
            command, cwd=project, env=env, check=True, text=True, capture_output=capture
        )
    # Retain live pip output, bound the whole tooling operation, and explain silence.
    install_env = env.copy()
    install_env["PYTHONUNBUFFERED"] = "1"
    install_env["PIP_KEYRING_PROVIDER"] = "disabled"
    install_env["PIP_NO_INPUT"] = "1"
    finished = threading.Event()
    started = time.monotonic()

    def progress():
        while not finished.wait(15):
            elapsed = int(time.monotonic() - started)
            print(
                f"Poetry tooling installation is still running ({elapsed}s; maximum 300s).",
                flush=True,
            )

    watcher = threading.Thread(target=progress, daemon=True)
    print(
        "Installing Poetry tooling; network access may be required (maximum 300s).",
        flush=True,
    )
    watcher.start()
    try:
        result = subprocess.run(
            command,
            cwd=project,
            env=install_env,
            check=True,
            text=True,
            capture_output=capture,
            timeout=300,
        )
        print("Poetry tooling installation completed.", flush=True)
        return result
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(
            "Poetry tooling installation exceeded 300 seconds and was stopped. "
            "Check access to your configured Python package index, proxy and certificate settings. "
            "If your index requires credentials, configure approved non-interactive credentials "
            "before rerunning python tools/setup.py. TLS verification remains enabled."
        ) from exc
    finally:
        finished.set()
        watcher.join()


def clean_environment():
    env = os.environ.copy()
    for name in ("VIRTUAL_ENV", "CONDA_PREFIX", "CONDA_DEFAULT_ENV", "PYTHONHOME"):
        env.pop(name, None)
    return env


def shared_poetry_root():
    """Return the versioned, user-owned tooling environment, never a project venv."""
    configured = os.environ.get("ROBO_POETRY_HOME")
    home = (
        Path(configured).expanduser()
        if configured
        else Path.home() / ".robo" / "poetry"
    )
    return home.resolve() / f"poetry-{POETRY_VERSION}"


@contextmanager
def shared_poetry_lock(root, timeout=360):
    """Serialize provisioning across processes; OS locks are released on exit/crash."""
    root.parent.mkdir(parents=True, exist_ok=True)
    with root.with_name(root.name + ".lock").open("a+b") as handle:
        handle.seek(0, os.SEEK_END)
        if handle.tell() == 0:
            handle.write(b"0")
            handle.flush()
        started = time.monotonic()
        while True:
            try:
                handle.seek(0)
                if os.name == "nt":
                    import msvcrt

                    msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
                else:
                    import fcntl

                    fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except OSError as exc:
                if time.monotonic() - started >= timeout:
                    raise RuntimeError(
                        f"Timed out waiting for shared Poetry tooling: {root}"
                    ) from exc
                threading.Event().wait(0.2)
        try:
            yield
        finally:
            handle.seek(0)
            if os.name == "nt":
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def _poetry_python(target=None, *, require_ready=True):
    root = shared_poetry_root()
    ready = (root / '.ready').is_file()
    candidates = [python_in(root)] if ready or not require_ready else []
    if require_ready:
        candidates.extend([Path(sys.executable), Path(getattr(sys, '_base_executable', sys.executable))])
        executable = shutil.which('poetry')
        if executable:
            executable = Path(executable).resolve()
            candidates.extend([
                python_in(executable.parent.parent),
                executable.parent / Path(sys.executable).name,
                executable.parent.parent / Path(sys.executable).name,
            ])
            poetry_home = os.environ.get('POETRY_HOME')
            if poetry_home:
                candidates.append(python_in(Path(poetry_home).expanduser() / 'venv'))
            if os.name == 'nt':
                data_home = Path(os.environ.get('APPDATA', Path.home() / 'AppData' / 'Roaming'))
            elif sys.platform == 'darwin':
                data_home = Path.home() / 'Library' / 'Application Support'
            else:
                data_home = Path(os.environ.get('XDG_DATA_HOME', Path.home() / '.local' / 'share'))
            candidates.append(python_in(data_home / 'pypoetry' / 'venv'))
    seen = set()
    for candidate in candidates:
        candidate = candidate.absolute()
        if any(part in ('.venv', '.venv-core') for part in candidate.parts):
            continue
        if target is not None and candidate.is_relative_to(Path(target).absolute()):
            continue
        if require_ready and not ready and candidate.is_relative_to(root.absolute()):
            continue
        if not candidate.is_file() or str(candidate) in seen:
            continue
        seen.add(str(candidate))
        try:
            result = subprocess.run(
                [str(candidate), "-m", "poetry", "--version"],
                env=clean_environment(),
                capture_output=True,
                text=True,
                check=False,
                timeout=15,
            )
        except (OSError, subprocess.TimeoutExpired):
            continue
        if (
            result.returncode == 0
            and f"Poetry (version {POETRY_VERSION})" in result.stdout
            and tool_certificates_are_secure(candidate)
        ):
            return candidate
    return None


def ensure_shared_poetry(project, *, bootstrap=True, timeout=30):
    """Select or provision pinned tooling independently of application packages."""
    root = shared_poetry_root()
    if root.is_relative_to(Path(project).resolve()):
        raise RuntimeError("ROBO_POETRY_HOME must be outside the project directory.")
    tool_python = _poetry_python()
    if tool_python is not None:
        return tool_python
    if not bootstrap:
        raise RuntimeError(
            f"Poetry {POETRY_VERSION} with certifi>=2026.10.19 is required. Run the project setup script first (Appian: --bootstrap-poetry)."
        )
    with shared_poetry_lock(root):
        tool_python = _poetry_python()
        if tool_python is not None:
            return tool_python
        (root / '.ready').unlink(missing_ok=True)
        tool_python = python_in(root)
        if not tool_python.is_file():
            venv.EnvBuilder(with_pip=True).create(root)
        run(secure_pip_command(tool_python, timeout), project, clean_environment())
        run(
            [
                str(tool_python),
                "-m",
                "pip",
                "install",
                "--upgrade",
                "--disable-pip-version-check",
                "--no-input",
                "--verbose",
                "--retries",
                "1",
                "--timeout",
                str(max(timeout, 1)),
                f"poetry=={POETRY_VERSION}",
                CERTIFI_REQUIREMENT,
            ],
            project,
            clean_environment(),
        )
        if _poetry_python(require_ready=False) is None:
            raise RuntimeError(
                f"Shared Poetry verification failed: {root}. Rerun setup to repair tooling."
            )
        (root / '.ready').write_text(f'Poetry {POETRY_VERSION}\n', encoding='ascii')
        return tool_python


@contextmanager
def managed_environment(project, directory=".venv", *, bootstrap=True, timeout=30):
    """Select and verify the exact project environment, never a cached fallback.

    Existing project environments are reused. Missing ones are created at the
    explicit target with the pinned Poetry 2.5.1 environment builder. A foreign
    active environment or cached Poetry association cannot redirect operations.
    """
    project = Path(project).resolve()
    target = project / directory
    python = python_in(target)
    existed = target.exists()
    if existed and (
        not python.is_file() or not (target / "pyvenv.cfg").is_file()
    ):
        raise RuntimeError(f"Incomplete environment: {target}. Repair it before setup.")
    tool_python = ensure_shared_poetry(project, bootstrap=bootstrap, timeout=timeout)
    command = [str(tool_python), "-m", "poetry", "--no-interaction"]
    env = clean_environment()
    env["POETRY_VIRTUALENVS_CREATE"] = "true"
    env["POETRY_VIRTUALENVS_IN_PROJECT"] = "true" if directory == ".venv" else "false"
    env["POETRY_VIRTUALENVS_OPTIONS_NO_PIP"] = "false"
    if not existed:
        builder = (
            "from pathlib import Path; import sys; "
            "from poetry.utils.env import EnvManager; "
            "EnvManager.build_venv(Path(sys.argv[1]), "
            "executable=Path(sys.argv[2]), with_pip=True)"
        )
        run([str(tool_python), "-c", builder, str(target),
             str(getattr(sys, "_base_executable", sys.executable))], project, env)
    if not python.is_file():
        raise RuntimeError(f"Poetry did not create the expected interpreter: {python}")
    run([str(python), "-c",
         "import sys; from pathlib import Path; "
         "assert sys.version_info[:2] == (3,12), 'Project environment requires Python 3.12'; "
         "assert Path(sys.prefix).resolve() == Path(sys.argv[1]).resolve(), 'Interpreter belongs to a different environment'",
         str(target)], project, env)
    env["VIRTUAL_ENV"] = str(target)
    env["PATH"] = str(python.parent) + os.pathsep + env.get("PATH", "")
    env["POETRY_VIRTUALENVS_CREATE"] = "false"
    selected = run([*command, "env", "info", "--path"], project, env, capture=True).stdout.strip()
    if Path(selected).resolve() != target.resolve():
        raise RuntimeError(f"Poetry selected {selected!r}; expected {target}. No packages were installed.")
    print(f"Project environment: {target} ({'reused' if existed else 'created'})", flush=True)
    print(f"Project interpreter: {python}", flush=True)
    print(f"Poetry tooling: {tool_python}", flush=True)
    yield python, command, env


def retain_poetry_tool(python, project, env):
    """Compatibility hook: publishing uses shared tooling, not project-local Poetry."""
    ensure_shared_poetry(project, bootstrap=False)


# Project-specific setup.
import argparse
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]

def main(argv=None):
    parser = argparse.ArgumentParser(prog=globals().get("_SETUP_PROG", str(Path(__file__).resolve())), description="Set up public documentation with Python 3.12 and Poetry 2.5.1.")
    actions = parser.add_mutually_exclusive_group()
    actions.add_argument("--build", action="store_true", help="Build the site with strict MkDocs checks after installation.")
    actions.add_argument("--serve", action="store_true", help="Start a local preview after installation.")
    parser.add_argument("--dev-addr", default="127.0.0.1:8000", help="Preview address, used with --serve (default: %(default)s).")
    args = parser.parse_args(argv)
    if sys.version_info[:2] != (3, 12):
        parser.error("Run setup with Python 3.12.")
    with managed_environment(PROJECT_ROOT) as (python, poetry, env):
        retain_poetry_tool(python, PROJECT_ROOT, env)
        secure_locked_certifi(poetry, PROJECT_ROOT, env)
        for command in (["lock"], ["check", "--lock"], ["install"]):
            run([*poetry, *command], PROJECT_ROOT, env)
            if command[0] == "lock":
                secure_locked_certifi(poetry, PROJECT_ROOT, env)
        if args.build:
            run([*poetry, "run", "mkdocs", "build", "--strict"], PROJECT_ROOT, env)
        elif args.serve:
            run([*poetry, "run", "mkdocs", "serve", "--dev-addr", args.dev_addr], PROJECT_ROOT, env)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
