from pathlib import Path
import subprocess
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def run(command: list[str]) -> None:
    result = subprocess.run(
        command,
        cwd=PROJECT_ROOT,
    )

    if result.returncode != 0:
        raise SystemExit(result.returncode)


def main() -> None:
    print("=" * 80)
    print("CHECKING STAGED DIFF")
    print("=" * 80)

    run(
        [
            "git",
            "diff",
            "--cached",
            "--check",
        ]
    )

    print()
    print("=" * 80)
    print("RUNNING TESTS")
    print("=" * 80)

    run(
        [
            sys.executable,
            "-m",
            "pytest",
            "tests",
            "-q",
        ]
    )

    print()
    print("=" * 80)
    print("READY TO COMMIT")
    print("=" * 80)


if __name__ == "__main__":
    main()