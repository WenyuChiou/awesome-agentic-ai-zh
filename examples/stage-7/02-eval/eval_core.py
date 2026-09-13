"""Shared, provider-neutral Eval runner for the Stage 7 teaching example."""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import tempfile
from collections import defaultdict
from pathlib import Path
from typing import Any, Callable


DEFAULT_DATASET_PATH = Path(__file__).with_name("eval_cases.json")
VALID_SPLITS = {"dev", "holdout"}
VALID_GRADERS = {"substring", "exact", "regex", "llm_judge"}
MAX_TRIALS = 20


def require_text(value: str | None, label: str) -> str:
    """Return usable model text or fail closed."""
    text = (value or "").strip()
    if not text:
        raise ValueError(f"{label} returned empty text")
    return text


def parse_verdict(verdict: str) -> bool:
    """Accept only a complete PASS or FAIL Judge response."""
    match = re.fullmatch(r"(PASS|FAIL)", verdict.strip(), re.IGNORECASE)
    if not match:
        raise ValueError("Judge must reply with exactly PASS or FAIL")
    return match.group(1).upper() == "PASS"


def load_dataset(path: str | Path = DEFAULT_DATASET_PATH) -> dict[str, Any]:
    """Load and validate the versioned teaching dataset."""
    dataset = json.loads(Path(path).read_text(encoding="utf-8"))
    return validate_dataset(dataset)


def validate_dataset(dataset: Any) -> dict[str, Any]:
    """Validate every field before a model or Judge can be called."""
    if not isinstance(dataset, dict):
        raise ValueError("dataset must be a JSON object")
    version = dataset.get("dataset_version")
    cases = dataset.get("cases")
    if (
        not isinstance(version, str)
        or not version.strip()
        or version != version.strip()
    ):
        raise ValueError("dataset_version must be a trimmed, non-empty string")
    if not isinstance(cases, list) or not cases:
        raise ValueError("cases must be a non-empty list")

    required = {
        "id",
        "split",
        "category",
        "input",
        "success_criteria",
        "grader",
        "source",
    }
    seen_ids: set[str] = set()
    seen_splits: set[str] = set()
    for case in cases:
        if not isinstance(case, dict) or not required <= case.keys():
            raise ValueError(f"each case must contain: {', '.join(sorted(required))}")
        case_id = case["id"]
        if (
            not isinstance(case_id, str)
            or not case_id.strip()
            or case_id != case_id.strip()
            or case_id in seen_ids
        ):
            raise ValueError("case ids must be trimmed, non-empty, and unique")
        seen_ids.add(case_id)
        split = case["split"]
        if not isinstance(split, str) or split not in VALID_SPLITS:
            raise ValueError(f"case {case_id}: split must be dev or holdout")
        seen_splits.add(split)
        for field in ("category", "input", "source"):
            value = case[field]
            if (
                not isinstance(value, str)
                or not value.strip()
                or value != value.strip()
            ):
                raise ValueError(
                    f"case {case_id}: {field} must be a trimmed, non-empty string"
                )
        criteria = case["success_criteria"]
        if (
            not isinstance(criteria, list)
            or not criteria
            or not all(
                isinstance(item, str) and item.strip() and item == item.strip()
                for item in criteria
            )
        ):
            raise ValueError(
                f"case {case_id}: success_criteria must be a non-empty string list"
            )
        grader = case["grader"]
        grader_type = grader.get("type") if isinstance(grader, dict) else None
        if not isinstance(grader_type, str) or grader_type not in VALID_GRADERS:
            raise ValueError(f"case {case_id}: unsupported grader")
        if (
            not isinstance(grader.get("value"), str)
            or not grader["value"].strip()
            or grader["value"] != grader["value"].strip()
        ):
            raise ValueError(f"case {case_id}: grader.value must be a non-empty string")
        if grader_type == "regex":
            try:
                re.compile(grader["value"])
            except re.error as error:
                raise ValueError(
                    f"case {case_id}: invalid regular expression"
                ) from error
    if seen_splits != VALID_SPLITS:
        raise ValueError("dataset must contain both dev and holdout cases")
    return dataset


def select_cases(dataset: dict[str, Any], split: str) -> list[dict[str, Any]]:
    """Select a named split without mutating the dataset."""
    if split == "all":
        return list(dataset["cases"])
    if split not in VALID_SPLITS:
        raise ValueError("split must be dev, holdout, or all")
    return [case for case in dataset["cases"] if case["split"] == split]


def grade_output(
    output: str | None,
    case: dict[str, Any],
    judge_fn: Callable[[str, dict[str, Any]], str] | None = None,
) -> bool:
    """Apply the case's grader. Empty model output is always a failure."""
    text = (output or "").strip()
    if not text:
        return False
    grader = case["grader"]
    grader_type = grader["type"]
    expected = grader["value"]
    if grader_type == "substring":
        return expected.casefold() in text.casefold()
    if grader_type == "exact":
        return text.casefold() == expected.strip().casefold()
    if grader_type == "regex":
        return re.fullmatch(expected, text) is not None
    if judge_fn is None:
        raise ValueError("llm_judge requires an explicit judge_fn")
    return parse_verdict(require_text(judge_fn(text, case), "Judge"))


def _category_summary(
    results: list[dict[str, Any]],
) -> dict[str, dict[str, float | int]]:
    counts: dict[str, dict[str, int]] = defaultdict(lambda: {"passed": 0, "total": 0})
    for result in results:
        category = counts[result["category"]]
        category["total"] += 1
        category["passed"] += int(result["passed"])
    return {
        name: {**values, "pass_rate": values["passed"] / values["total"]}
        for name, values in sorted(counts.items())
    }


def compare_to_baseline(
    report: dict[str, Any], baseline: dict[str, Any]
) -> dict[str, int]:
    """Compare like with like; mismatched datasets fail instead of guessing."""
    validate_baseline(
        baseline,
        dataset_version=report["dataset_version"],
        split=report["split"],
        case_ids=report["case_ids"],
    )

    comparison = {"improved": 0, "same": 0, "regressed": 0}
    for case_id, current_rate in report["case_pass_rates"].items():
        previous_rate = baseline["case_pass_rates"][case_id]
        if current_rate > previous_rate:
            comparison["improved"] += 1
        elif current_rate < previous_rate:
            comparison["regressed"] += 1
        else:
            comparison["same"] += 1
    return comparison


def validate_baseline(
    baseline: Any,
    *,
    dataset_version: str,
    split: str,
    case_ids: list[str],
) -> None:
    """Reject an incompatible baseline before any provider work begins."""
    if not isinstance(baseline, dict):
        raise ValueError("baseline report must be a JSON object")
    expected = {
        "dataset_version": dataset_version,
        "split": split,
        "case_ids": case_ids,
    }
    for field in ("dataset_version", "split", "case_ids"):
        if baseline.get(field) != expected[field]:
            raise ValueError(f"baseline {field} does not match this run")
    baseline_rates = baseline.get("case_pass_rates")
    if not isinstance(baseline_rates, dict) or set(baseline_rates) != set(case_ids):
        raise ValueError("baseline case_pass_rates do not match this run")
    if not all(
        isinstance(rate, (int, float))
        and not isinstance(rate, bool)
        and math.isfinite(rate)
        and 0 <= rate <= 1
        for rate in baseline_rates.values()
    ):
        raise ValueError("baseline case_pass_rates must be numbers from 0 to 1")


def run_eval(
    dataset: dict[str, Any],
    agent_fn: Callable[[str], str | None],
    *,
    split: str = "dev",
    trials: int = 1,
    model: str = "unknown",
    provider: str = "unknown",
    judge_fn: Callable[[str, dict[str, Any]], str] | None = None,
    baseline: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Run every selected case one or more times and return auditable evidence."""
    validate_dataset(dataset)
    if not 1 <= trials <= MAX_TRIALS:
        raise ValueError(f"trials must be from 1 to {MAX_TRIALS}")
    cases = select_cases(dataset, split)
    case_ids = [case["id"] for case in cases]
    if baseline is not None:
        validate_baseline(
            baseline,
            dataset_version=dataset["dataset_version"],
            split=split,
            case_ids=case_ids,
        )
    trial_reports: list[dict[str, Any]] = []
    all_results: list[dict[str, Any]] = []

    for trial_number in range(1, trials + 1):
        results = []
        for case in cases:
            raw_output = agent_fn(case["input"])
            output = (raw_output or "").strip()
            passed = grade_output(output, case, judge_fn)
            result = {
                "id": case["id"],
                "category": case["category"],
                "grader": case["grader"]["type"],
                "passed": passed,
                "output": output,
            }
            results.append(result)
            all_results.append(result)
        passed_count = sum(int(result["passed"]) for result in results)
        trial_reports.append(
            {
                "trial": trial_number,
                "passed": passed_count,
                "total": len(results),
                "pass_rate": passed_count / len(results),
                "results": results,
            }
        )

    case_pass_rates = {
        case["id"]: sum(
            int(result["passed"])
            for result in all_results
            if result["id"] == case["id"]
        )
        / trials
        for case in cases
    }
    passed_count = sum(int(result["passed"]) for result in all_results)
    report: dict[str, Any] = {
        "dataset_version": dataset["dataset_version"],
        "split": split,
        "model": model,
        "provider": provider,
        "trial_count": trials,
        "trials": trial_reports,
        "case_ids": case_ids,
        "case_pass_rates": case_pass_rates,
        "categories": _category_summary(all_results),
        "failures": [
            {"trial": trial["trial"], **result}
            for trial in trial_reports
            for result in trial["results"]
            if not result["passed"]
        ],
        "passed": passed_count,
        "total_attempts": len(all_results),
        "pass_rate": passed_count / len(all_results),
        "improved": 0,
        "same": 0,
        "regressed": 0,
    }
    if baseline is not None:
        report.update(compare_to_baseline(report, baseline))
    return report


def load_report(path: str | Path) -> dict[str, Any]:
    """Load a previous report for baseline comparison."""
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("baseline report must be a JSON object")
    return value


def save_report(report: dict[str, Any], path: str | Path) -> Path:
    """Atomically save a report only when the user requests it."""
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="\n",
            dir=destination.parent,
            prefix=f".{destination.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temporary = Path(handle.name)
            json.dump(report, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, destination)
    except Exception:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
        raise
    return destination


def _positive_int(value: str) -> int:
    parsed = int(value)
    if not 1 <= parsed <= MAX_TRIALS:
        raise argparse.ArgumentTypeError(f"must be from 1 to {MAX_TRIALS}")
    return parsed


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the Stage 7 Eval teaching suite.")
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET_PATH)
    parser.add_argument("--split", choices=("dev", "holdout", "all"), default="dev")
    parser.add_argument("--trials", type=_positive_int, default=1)
    parser.add_argument("--save-report", type=Path)
    parser.add_argument("--baseline", type=Path)
    return parser


def run_cli(
    agent_fn: Callable[[str], str | None],
    *,
    model: str,
    provider: str,
    judge_fn: Callable[[str, dict[str, Any]], str] | None = None,
    argv: list[str] | None = None,
) -> int:
    """Run the shared CLI for one provider."""
    args = build_parser().parse_args(argv)
    try:
        if (
            args.baseline is not None
            and args.save_report is not None
            and args.baseline.resolve() == args.save_report.resolve()
        ):
            raise ValueError("baseline and save-report must use different files")
        dataset = load_dataset(args.dataset)
        baseline = load_report(args.baseline) if args.baseline else None
        report = run_eval(
            dataset,
            agent_fn,
            split=args.split,
            trials=args.trials,
            model=model,
            provider=provider,
            judge_fn=judge_fn,
            baseline=baseline,
        )
        if args.save_report:
            saved = save_report(report, args.save_report)
            print(f"Saved report: {saved}")
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"Eval stopped: {error}")
        return 2

    print(
        f"{provider}/{model} · {report['split']} · "
        f"{report['passed']}/{report['total_attempts']} passed "
        f"({report['pass_rate']:.0%})"
    )
    for failure in report["failures"]:
        print(
            f"FAIL trial={failure['trial']} id={failure['id']} category={failure['category']}"
        )
    if baseline is not None:
        print(
            "Compared with baseline: "
            f"{report['improved']} improved, {report['same']} same, "
            f"{report['regressed']} regressed"
        )
    return 0
