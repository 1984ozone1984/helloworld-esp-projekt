import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "target"))

from dutfixtures import *  # noqa: E402,F401,F403  (fixtures shared with tests/target)
