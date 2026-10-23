"""Set up this project's Poetry environment from any working directory."""
from pathlib import Path
import runpy
import sys

if __name__ == "__main__":
    tools = Path(__file__).resolve().parents[1] / "tools"
    sys.path.insert(0, str(tools))
    runpy.run_path(
        str(tools / 'setup_docs.py'),
        init_globals={"_SETUP_PROG": sys.argv[0]},
        run_name="__main__",
    )
