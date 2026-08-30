"""Run every Stage 06 example test in isolation.

The example folders intentionally reuse names such as ``test.py`` and
``starter.py``. Running one subprocess per folder prevents Python's module cache
from mixing those files together and gives beginners one reliable command.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples" / "stage-6"
FOLDERS = [
    "01-embeddings",
    "02-vector-db",
    "03-chunking-comparison",
    "04-full-rag-pipeline",
    "05-long-term-memory",
]
TEST_FILES = ["test.py", "test_anthropic.py"]


def main() -> int:
    failures: list[str] = []
    for folder_name in FOLDERS:
        folder = EXAMPLES / folder_name
        for test_name in TEST_FILES:
            label = f"{folder_name}/{test_name}"
            print(f"\n=== {label} ===", flush=True)
            result = subprocess.run(
                [sys.executable, test_name],
                cwd=folder,
                check=False,
                timeout=60,
            )
            if result.returncode != 0:
                failures.append(label)

    if failures:
        print("\nFAILED: " + ", ".join(failures))
        return 1
    print("\nAll 10 Stage 06 example checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
