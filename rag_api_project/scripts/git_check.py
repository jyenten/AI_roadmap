import subprocess
import sys

def run_command(
    command: list[str],
    description: str,
) -> bool:
    print()
    print("=" * 80)
    print(description)
    print("=" * 80)

    result = subprocess.run(
        command,
        text=True
    )

    return result.returncode == 0

def main() -> None:
    checks = [
        (
            [
                "git",
                "diff",
                "--cached",
                "--check",
            ],
            "Checking staged diff...",
        ),
        (
            [
                sys.executable,
                "-m",
                "pytest",
                "tests",
                "-q",
            ],
            "Running tests...",
        ),
    ]

    for command, description in checks:
        success = run_command(
            command,
            description,
        )

        if not success:
            print()
            print("COMMIT CHECK FAILED")
            sys.exit(1)

    print()
    print("=" * 80)
    print("READY TO COMMIT")
    print("=" * 80)


if __name__ == "__main__":
    main()