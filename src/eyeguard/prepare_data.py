"""Create a private, analysis-ready CSV from the Google Forms workbook."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT = PROJECT_ROOT / "data" / "raw" / "survey_responses.xlsx"
DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "processed" / "responses_clean.csv"

SYMPTOM_VALUES = {
    "Never": 0,
    "Sometimes": 1,
    "Often": 2,
    "Always": 3,
}

SYMPTOM_COLUMNS = {
    "Eye strain or tiredness": "symptom_eye_strain",
    "Headache": "symptom_headache",
    "Blurred vision": "symptom_blurred_vision",
    "Dry or irritated eyes": "symptom_dry_eyes",
    "Difficulty focusing after screen use": "symptom_difficulty_focusing",
}


def _column_for_prefix(columns: list[str], prefix: str) -> str:
    matches = [column for column in columns if column.strip().startswith(prefix)]
    if len(matches) != 1:
        raise ValueError(
            f"Expected one survey column beginning with {prefix!r}; found {len(matches)}."
        )
    return matches[0]


def _symptom_label(column: str) -> str:
    match = re.search(r"\[([^\]]+)\]\s*$", column.strip())
    if not match:
        raise ValueError(f"Could not identify the symptom name in column {column!r}.")
    return match.group(1).strip()


def prepare_data(input_path: Path, output_path: Path) -> dict[str, int | float]:
    if not input_path.exists():
        raise FileNotFoundError(
            f"Survey workbook not found: {input_path}\n"
            "Place it at data/raw/survey_responses.xlsx or pass --input."
        )

    raw = pd.read_excel(input_path, sheet_name=0, dtype="string")
    columns = list(raw.columns)

    upload_columns = [
        column
        for column in columns
        if column.strip().startswith("Upload Weekly Screen-Time Screenshot")
    ]
    if len(upload_columns) != 1:
        raise ValueError(
            "Expected one weekly screen-time screenshot upload field; "
            f"found {len(upload_columns)}. Check the survey export columns."
        )

    symptom_source_columns = [
        column
        for column in columns
        if column.strip().startswith(
            "How frequently do you experience the following symptoms"
        )
    ]
    if len(symptom_source_columns) != len(SYMPTOM_COLUMNS):
        raise ValueError(
            f"Expected {len(SYMPTOM_COLUMNS)} symptom questions; "
            f"found {len(symptom_source_columns)}."
        )

    rename = {
        _column_for_prefix(columns, "Age Group"): "age_group",
        _column_for_prefix(
            columns,
            "On average, how many hours do you spend actively using screens each day?",
        ): "screen_time_category",
        _column_for_prefix(
            columns, "On average, How many hours of sleep do you get per night?"
        ): "sleep_category",
        _column_for_prefix(
            columns,
            "How many short breaks (looking away from the screen) do you take",
        ): "breaks_per_hour_category",
        _column_for_prefix(columns, "What device do you use most"): "primary_device",
        _column_for_prefix(columns, "Do you wear glasses or contact lenses"): "vision_correction",
    }

    for source_column in symptom_source_columns:
        label = _symptom_label(source_column)
        if label not in SYMPTOM_COLUMNS:
            raise ValueError(f"Unexpected symptom question: {label!r}.")
        rename[source_column] = SYMPTOM_COLUMNS[label]

    missing_symptoms = set(SYMPTOM_COLUMNS.values()) - set(rename.values())
    if missing_symptoms:
        raise ValueError(f"Missing symptom questions: {sorted(missing_symptoms)}")

    clean = raw.drop(columns=upload_columns).rename(columns=rename).copy()
    symptom_columns = list(SYMPTOM_COLUMNS.values())
    symptom_answers = clean[symptom_columns].apply(lambda series: series.str.strip())
    scored_answers = symptom_answers.replace(SYMPTOM_VALUES)

    invalid_answers = scored_answers.isna()
    if invalid_answers.any().any():
        invalid_count = int(invalid_answers.sum().sum())
        raise ValueError(
            f"Found {invalid_count} blank or unrecognized symptom answers. "
            "Review the source export before scoring."
        )

    clean[symptom_columns] = symptom_answers
    clean["exploratory_symptom_score"] = scored_answers.astype("int64").sum(axis=1)
    clean["duplicate_candidate"] = clean.duplicated(
        subset=[column for column in clean.columns if column != "exploratory_symptom_score"],
        keep=False,
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    clean.to_csv(output_path, index=False, encoding="utf-8")

    duplicate_rows = int(clean["duplicate_candidate"].sum())
    summary: dict[str, int | float] = {
        "responses": len(clean),
        "analysis_columns": len(clean.columns),
        "missing_cells": int(clean.isna().sum().sum()),
        "duplicate_candidate_rows": duplicate_rows,
        "symptom_score_mean": round(float(clean["exploratory_symptom_score"].mean()), 2),
        "symptom_score_median": float(clean["exploratory_symptom_score"].median()),
    }
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    summary = prepare_data(args.input, args.output)
    print("Prepared survey data:")
    for name, value in summary.items():
        print(f"  {name}: {value}")
    print(f"  output: {args.output}")
    print("  screenshot upload references: excluded")
    print("  duplicate candidates: flagged, not removed")


if __name__ == "__main__":
    main()
