"""Set up the public documentation project with Poetry."""
from pathlib import Path
import runpy
import sys

if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent / "tools"))
    runpy.run_path(str(Path(__file__).resolve().parent / "tools" / "setup_docs.py"), init_globals={"_SETUP_PROG": sys.argv[0]}, run_name="__main__")
