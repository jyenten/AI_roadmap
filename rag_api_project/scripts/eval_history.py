import json

from pathlib import Path

def save_bounded_history(
        path: Path,
        result: dict,
        max_runs: int = 10,
) -> None:
    if max_runs <= 0:
        raise ValueError(
            "max_runs must be greater than 0"
        )

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    runs = []

    if path.exists():
        with path.open(
            "r",
            encoding="utf-8",
        ) as file:
            for line in file:
                line = line.strip()

                if line:
                    runs.append(
                        json.loads(line)
                    )

    runs.append(result)

    runs = runs[-max_runs:]

    with path.open(
        "w",
        encoding="utf-8",
    ) as file:
        for run in runs:
            file.write(
                json.dumps(
                    run,
                    ensure_ascii=False,
                )
                + "\n"
            )