"""Poetry environment setup and local documentation preview."""
import argparse
from pathlib import Path
import sys
from poetry_environment import managed_environment, retain_poetry_tool, run

PROJECT_ROOT = Path(__file__).resolve().parents[1]

def main(argv=None):
    parser = argparse.ArgumentParser(prog=globals().get("_SETUP_PROG"), description="Set up public documentation with Python 3.12 and Poetry 2.5.1.")
    actions = parser.add_mutually_exclusive_group()
    actions.add_argument("--build", action="store_true", help="Build the site with strict MkDocs checks after installation.")
    actions.add_argument("--serve", action="store_true", help="Start a local preview after installation.")
    parser.add_argument("--dev-addr", default="127.0.0.1:8000", help="Preview address, used with --serve (default: %(default)s).")
    args = parser.parse_args(argv)
    if sys.version_info[:2] != (3, 12):
        parser.error("Run setup with Python 3.12.")
    with managed_environment(PROJECT_ROOT) as (python, poetry, env):
        retain_poetry_tool(python, PROJECT_ROOT, env)
        for command in (["lock"], ["check", "--lock"], ["install"]):
            run([*poetry, *command], PROJECT_ROOT, env)
        if args.build:
            run([*poetry, "run", "mkdocs", "build", "--strict"], PROJECT_ROOT, env)
        elif args.serve:
            run([*poetry, "run", "mkdocs", "serve", "--dev-addr", args.dev_addr], PROJECT_ROOT, env)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
