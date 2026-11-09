#!/usr/bin/env python3
"""Deploy CTE-HF-AI: create venv, install, run tests."""

import subprocess
import sys
from pathlib import Path


def main() -> int:
    repo = Path(__file__).resolve().parent
    venv = repo / ".venv"
    if not venv.exists():
        subprocess.run([sys.executable, "-m", "venv", str(venv)], check=True)
    py = venv / "bin" / "python"
    subprocess.run([str(py), "-m", "pip", "install", "--upgrade",
                    "pip", "setuptools", "wheel"], check=True)
    subprocess.run([str(py), "-m", "pip", "install", "-e", ".[dev]"],
                   cwd=repo, check=True)
    subprocess.run([str(py), "-m", "pytest"], cwd=repo, check=True)
    print(f"\nDone. Activate with:\n  source {venv}/bin/activate")
    return 0


if __name__ == "__main__":
    sys.exit(main())
