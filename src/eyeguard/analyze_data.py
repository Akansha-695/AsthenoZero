"""Print aggregate summaries of the prepared survey data."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
INPUT_PATH = PROJECT_ROOT / "data" / "processed" / "responses_clean.csv"

PROFILE_ORDERS = {
    "age_group": ["15-18", "19-24", "25-34", "35-45", "45+"],
    "screen_time_category": [
        "Less than 2 hours",
        "2-4 hours",
        "4-6 hours",
        "6-8 hours",
        "More than 8 hours",
    ],
    "sleep_category": [
        "Less than 5 hours",
        "5-6 hours",
        "6-7 hours",
        "7-8 hours",
        "More than 8 hours",
    ],
    "breaks_per_hour_category": ["0", "1-2", "2-3", "4-5", "5 or more"],
    "primary_device": ["Phone", "Laptop / PC", "Tab", "All roughly equal"],
    "vision_correction": ["No", "Yes"],
}

SYMPTOM_COLUMNS = [
    "symptom_eye_strain",
    "symptom_headache",
    "symptom_blurred_vision",
    "symptom_dry_eyes",
    "symptom_difficulty_focusing",
]
SYMPTOM_ORDER = ["Never", "Sometimes", "Often", "Always"]


def _ordered_values(counts: pd.Series, expected_order: list[str]) -> list[str]:
    known = [value for value in expected_order if value in counts.index]
    other = [str(value) for value in counts.index if value not in expected_order]
    return known + other


def _print_distribution(
    title: str, values: pd.Series, expected_order: list[str] | None = None
) -> None:
    counts = values.value_counts(dropna=False)
    order = _ordered_values(counts, expected_order or [])
    counts = counts.reindex(order)
    print(f"\n{title}")
    for category, count in counts.items():
        percentage = 100 * int(count) / len(values)
        print(f"  {category}: {int(count)} ({percentage:.1f}%)")


def main() -> None:
    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Prepared file not found: {INPUT_PATH}. "
            "Run prepare_data.py first."
        )

    data = pd.read_csv(INPUT_PATH)
    required_columns = {
        "duplicate_candidate",
        "exploratory_symptom_score",
        "screen_time_category",
        *PROFILE_ORDERS.keys(),
        *SYMPTOM_COLUMNS,
    }
    missing_columns = required_columns - set(data.columns)
    if missing_columns:
        raise ValueError(f"Prepared file is missing columns: {sorted(missing_columns)}")

    print("Survey overview")
    print(f"  responses retained: {len(data)}")
    print(
        "  rows in duplicate-like group(s): "
        f"{int(data['duplicate_candidate'].astype(bool).sum())}"
    )
    print("  duplicate-like responses are retained, not automatically removed")

    for column, order in PROFILE_ORDERS.items():
        _print_distribution(column.replace("_", " ").title(), data[column], order)

    print("\nSymptom response frequencies")
    for column in SYMPTOM_COLUMNS:
        _print_distribution(column.replace("symptom_", "").replace("_", " ").title(), data[column], SYMPTOM_ORDER)

    score = pd.to_numeric(data["exploratory_symptom_score"], errors="raise")
    print("\nExploratory symptom score (project-created, range 0-15)")
    print(f"  mean: {score.mean():.2f}")
    print(f"  median: {score.median():.1f}")
    print(f"  minimum: {score.min():.0f}")
    print(f"  maximum: {score.max():.0f}")

    grouped = data.assign(exploratory_symptom_score=score).groupby(
        "screen_time_category", observed=False
    )["exploratory_symptom_score"]
    stats = grouped.agg(responses="size", mean_score="mean", median_score="median")
    order = [
        value
        for value in PROFILE_ORDERS["screen_time_category"]
        if value in stats.index
    ]
    stats = stats.reindex(order)
    print("\nExploratory score by screen-time category")
    for category, row in stats.iterrows():
        print(
            f"  {category}: n={int(row['responses'])}, "
            f"mean={row['mean_score']:.2f}, median={row['median_score']:.1f}"
        )

    print(
        "\nInterpretation note: these are descriptive, self-reported results. "
        "The score is not a validated clinical measure, and category summaries "
        "do not establish cause and effect."
    )


if __name__ == "__main__":
    main()
