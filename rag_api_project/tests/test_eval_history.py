import json

from scripts.eval_history import save_bounded_history

def test_save_bounded_history_keeps_last_10(
        tmp_path,
) -> None:
    history_path = tmp_path / "dev_runs.jsonl"

    for run_number in range(1, 12):
        save_bounded_history(
            history_path,
            {
                "run_number": run_number,
            },
            max_runs=10,

        )


    with history_path.open(
        "r",
        encoding="utf-8",
    ) as file:
        runs = [
            json.loads(line)
            for line in file
            if line.strip()
        ]

    assert len(runs) == 10
    assert runs[0]["run_number"] == 2
    assert runs[-1]["run_number"] == 11